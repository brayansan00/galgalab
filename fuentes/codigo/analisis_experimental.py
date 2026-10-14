"""Parte 2: tratamiento del ensayo (Viga4SamuelBrayan.csv). Salidas: figures/fig_exp_*.png y resultados_exp.json"""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
A = Path(__file__).resolve().parent; (A/"figures").mkdir(exist_ok=True)
E = 69000.0; sig_ana = 11.3985
t, e = [], []
for ln in open(next(p for p in (A/"Viga4SamuelBrayan.csv", A.parent/"datos"/"Viga4SamuelBrayan.csv") if p.exists()), encoding="utf-8-sig"):
    p = ln.strip().split(";")
    if len(p) != 2 or not p[1].strip() or p[0] == "Time": continue
    t.append(datetime.strptime(p[0], "%d/%m/%Y %H:%M:%S.%f")); e.append(float(p[1]))
t0 = t[0]; tt = np.array([(x - t0).total_seconds() for x in t]); eps = np.array(e) * 1e6      # µε
W = dict(base=(11.0, 16.5), plat=(24.0, 53.0))
mb = (tt >= W['base'][0]) & (tt <= W['base'][1]); mp = (tt >= W['plat'][0]) & (tt <= W['plat'][1])
m_end = (tt >= 66.0) & (tt <= tt[-1])   # reposo final 66-77 s
res = dict(n=len(tt), dt=float(np.median(np.diff(tt))), dur=float(tt[-1]), fs=float(1/np.median(np.diff(tt))),
           eps_ini=float(eps[tt <= 3].mean()), eps_base=float(eps[mb].mean()), n_base=int(mb.sum()),
           eps_plat=float(eps[mp].mean()), s_plat=float(eps[mp].std(ddof=1)), n_plat=int(mp.sum()),
           eps_fin=float(eps[m_end].mean()), eps_max=float(eps.max()))
res['eps_net'] = res['eps_plat'] - res['eps_base']
res['sigma_raw'] = E * res['eps_plat'] * 1e-6; res['sigma_net'] = E * res['eps_net'] * 1e-6
res['err_raw'] = (res['sigma_raw'] - sig_ana) / sig_ana * 100; res['err_net'] = (res['sigma_net'] - sig_ana) / sig_ana * 100
slope = np.polyfit(tt[mp], eps[mp], 1)[0]; res['pend_plat_ue_s'] = float(slope)
res['sem_plat_indep'] = res['s_plat'] / np.sqrt(res['n_plat'])            # solo si las muestras fueran independientes
res['s_base'] = float(eps[mb].std(ddof=1)); res['sem_dif_indep'] = float(np.hypot(res['sem_plat_indep'], res['s_base']/np.sqrt(res['n_base'])))
x = eps[mp] - eps[mp].mean()
res['autocorr_0p1s'] = float(np.dot(x[:-10], x[10:]) / np.dot(x, x)); res['autocorr_1s'] = float(np.dot(x[:-100], x[100:]) / np.dot(x, x))
json.dump(res, open(A.parent/"datos"/"resultados_exp.json", "w"), indent=1); print(json.dumps(res, indent=1))

C = dict(sig='#1f4e79', base='#d9822b', plat='#2a8f5f', gris='#666')
# Figura 1: señal completa con fases
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.axvspan(*W['base'], color=C['base'], alpha=.18, label='Línea base (11–16,5 s)')
ax.axvspan(*W['plat'], color=C['plat'], alpha=.18, label='Meseta con carga (24–53 s)')
ax.plot(tt, eps, color=C['sig'], lw=.9)
ax.hlines(res['eps_plat'], *W['plat'], color=C['plat'], lw=2); ax.hlines(res['eps_base'], *W['base'], color=C['base'], lw=2)
ax.annotate(f"promedio meseta = {res['eps_plat']:.1f} µε", (31, res['eps_plat']), xytext=(31, 232), arrowprops=dict(arrowstyle='-', color=C['gris']), fontsize=9, ha='left')
ax.annotate(f"base = {res['eps_base']:.1f} µε", (13.5, res['eps_base']), xytext=(6.5, 55), arrowprops=dict(arrowstyle='-', color=C['gris']), fontsize=9)
for x, s in ((3, 'Reposo'), (19.7, 'Rampa de carga'), (38, 'Carga P aplicada'), (60, 'Descarga'), (72, 'Reposo')): ax.text(x, -52, s, ha='center', fontsize=8, color=C['gris'])
ax.set_xlabel('Tiempo [s]'); ax.set_ylabel('Deformación ε [µε]'); ax.set_xlim(0, tt[-1]); ax.set_ylim(-65, 300)
ax.set_title('Ensayo con galga extensiométrica: deformación vs. tiempo'); ax.grid(alpha=.25); ax.legend(loc='upper right', fontsize=8, frameon=False, bbox_to_anchor=(1, .52))
fig.tight_layout(); fig.savefig(A/"figures"/"fig_exp_senal.png", dpi=200); plt.close()
# Figura 2: zoom de la meseta
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5), gridspec_kw=dict(width_ratios=[2, 1]))
ax[0].plot(tt[mp], eps[mp], color=C['sig'], lw=.7); ax[0].axhline(res['eps_plat'], color=C['plat'], lw=2)
ax[0].fill_between(tt[mp], res['eps_plat']-res['s_plat'], res['eps_plat']+res['s_plat'], color=C['plat'], alpha=.2, label=f"±1 desv. est. ({res['s_plat']:.2f} µε)")
ax[0].set_xlabel('Tiempo [s]'); ax[0].set_ylabel('ε [µε]'); ax[0].set_title('Meseta (n = %d muestras)' % res['n_plat']); ax[0].legend(fontsize=8, frameon=False); ax[0].grid(alpha=.25)
ax[1].hist(eps[mp], bins=40, color=C['sig'], alpha=.8); ax[1].axvline(res['eps_plat'], color=C['plat'], lw=2)
ax[1].set_xlabel('ε [µε]'); ax[1].set_ylabel('Muestras'); ax[1].set_title('Distribución'); ax[1].grid(alpha=.25)
fig.tight_layout(); fig.savefig(A/"figures"/"fig_exp_meseta.png", dpi=200); plt.close()
