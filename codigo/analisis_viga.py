"""
Análisis de la viga con galga (analítico + experimental + diagramas V y M)
Unidades: N, mm, MPa.  Cambie SOLO la sección PARÁMETROS cuando Samuel confirme las medidas.
"""
import math, os, sys, numpy as np
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------- PARÁMETROS (fuente: STEP VIGA_FEM.step salvo que se indique) ----------------
AQUI = Path(__file__).resolve().parent          # carpeta del script: el CSV debe estar aquí
CSV = next((p for p in (AQUI/"Viga4SamuelBrayan.csv", AQUI.parent/"datos"/"Viga4SamuelBrayan.csv") if p.exists()), AQUI/"Viga4SamuelBrayan.csv")
(AQUI / "figures").mkdir(exist_ok=True)
E = 69000.0                         # MPa, Aluminio 1100
g = 9.81                            # m/s2 (usar el mismo en todo el trabajo)
m_total = 5.0 + 0.073               # kg (pesa + tornillo y arandelas)
be, he, t = 70.0, 30.0, 1.0         # mm; eje débil: la altura que flecta es he = 30 (galga en la cara z=30)
L_total = 746.0
y_galga_ini, y_galga_fin = 198.0, 213.0     # mm, marca de galga en el STEP (5 x 15 mm)
y_carga = 711.0                     # mm, eje del agujero/tornillo en el STEP (Samuel midió 68,7 cm: por confirmar)
y_mordaza = 141.83                  # mm, borde libre de la mordaza en el STEP (Samuel midió 14,7 cm: por confirmar)

# ---------------- ANALÍTICO ----------------
P = m_total * g
Bi, Hi = be - 2*t, he - 2*t
I = (be*he**3 - Bi*Hi**3)/12
c = he/2
y_g = 0.5*(y_galga_ini + y_galga_fin)

def sigma_analitico(y_load, y_gauge=y_g, P=P):
    M = P*(y_load - y_gauge)
    return M*c/I, M

sig_a, M_g = sigma_analitico(y_carga)
print(f"P = {P:.3f} N | I = {I:.1f} mm4 | c = {c} mm | y_galga = {y_g} mm | brazo = {y_carga-y_g} mm")
print(f"M(galga) = {M_g:.0f} N·mm | sigma analítico = {sig_a:.3f} MPa | eps = {sig_a/E*1e6:.1f} µε")

# ---------------- EXPERIMENTAL ----------------
rows=[l.split(';') for l in open(CSV,encoding='utf-8-sig').read().splitlines()[1:]
      if l.count(';')==1 and l.split(';')[1].strip()]
t0=datetime.strptime(rows[0][0],'%d/%m/%Y %H:%M:%S.%f')
tt=np.array([(datetime.strptime(r[0],'%d/%m/%Y %H:%M:%S.%f')-t0).total_seconds() for r in rows])
ee=np.array([float(r[1]) for r in rows])*1e6          # µε
win_pl=(tt>=24)&(tt<=53)                              # meseta estable
win_base=(tt>=11)&(tt<=16.5)                          # línea base inmediatamente antes de cargar
eps_raw=ee[win_pl].mean(); eps_std=ee[win_pl].std(ddof=1); base=ee[win_base].mean()
eps_net=eps_raw-base
sig_raw, sig_net = E*eps_raw*1e-6, E*eps_net*1e-6
print(f"meseta = {eps_raw:.2f} µε (s={eps_std:.2f}, n={win_pl.sum()}) | base previa = {base:.2f} µε | neto = {eps_net:.2f} µε")
print(f"sigma exp cruda = {sig_raw:.3f} MPa | sigma exp con línea base = {sig_net:.3f} MPa")
for nm,s in (("cruda",sig_raw),("con línea base",sig_net)):
    print(f"  error exp ({nm}) vs analítico: {(s/sig_a-1)*100:+.1f} %")

# escenarios de posición (sensibilidad a las medidas por confirmar)
print("\nSensibilidad a la posición de carga/galga (σ analítico):")
for nm,yl,yg in [("STEP: carga 711, galga 205,5",711,205.5),("carga 707 (PDF/FEM), galga 205,5",707,205.5),
                 ("Samuel: brazo 491 mm",205.5+491,205.5),("Samuel: 687-491 hasta centro (brazo 483,5)",205.5+483.5,205.5)]:
    s,_=sigma_analitico(yl,yg); print(f"  {nm:45s} brazo={yl-yg:6.1f} mm  σ={s:6.3f} MPa  exp(línea base) {(sig_net/s-1)*100:+5.1f} %")

# incertidumbre (propagación lineal de M c / I)
u_brazo, u_t, u_E = 3.0, 0.05, 1000.0
dI_dt = (I - (be*he**3-(be-2*(t+1e-3))*(he-2*(t+1e-3))**3)/12)/1e-3      # dI/dt negativa
I_t2=(be*he**3-(be-2*(t+u_t))*(he-2*(t+u_t))**3)/12
print(f"\nEfecto del espesor ±{u_t} mm en σ analítico: {(I/I_t2-1)*100:+.1f} % (espesor +) ; brazo ±{u_brazo} mm: ±{u_brazo/(y_carga-y_g)*100:.1f} %")

# ---------------- FIGURAS ----------------
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
fig,ax=plt.subplots(figsize=(8,4))
ax.plot(tt,ee,lw=.8,color="#1f77b4",label="Señal del puente (galga)")
ax.axvspan(24,53,color="#2ca02c",alpha=.15,label=f"Ventana de promediado: {eps_raw:.1f} µε")
ax.axvspan(11,16.5,color="#ff7f0e",alpha=.2,label=f"Línea base previa: {base:.1f} µε")
ax.axhline(eps_raw,color="#2ca02c",lw=1,ls="--")
ax.set_xlabel("Tiempo [s]"); ax.set_ylabel("Deformación unitaria [µε]"); ax.legend(frameon=False,loc="center right")
ax.set_title("Resultado experimental: deformación en la galga"); fig.tight_layout(); fig.savefig(AQUI/"figures"/"fig_experimental.png",dpi=200)

# diagramas V y M (voladizo, carga en y_carga, apoyo en el borde de la mordaza)
x=np.linspace(y_mordaza,y_carga,400); M=P*(y_carga-x); V=np.full_like(x,P)
fig,axs=plt.subplots(3,1,figsize=(8,7.5),sharex=True,gridspec_kw={"height_ratios":[1,1.2,1.2]})
a=axs[0]; a.add_patch(plt.Rectangle((0,-3),L_total,6,fc="#d9d9d9",ec="k")); a.add_patch(plt.Rectangle((0,-8),y_mordaza,16,fc="#7f7f7f",alpha=.5))
a.text(y_mordaza/2,10,"mordaza",ha="center"); a.plot([y_g],[3],"s",color="crimson"); a.text(y_g,-12,f"galga\ny={y_g:.1f}",ha="center",color="crimson")
a.annotate("",xy=(y_carga,-30),xytext=(y_carga,-3),arrowprops=dict(arrowstyle="->",lw=2)); a.text(y_carga-10,-25,f"P={P:.2f} N",ha="right")
a.set_ylim(-35,18); a.set_yticks([]); a.spines["left"].set_visible(False); a.set_title("Viga en voladizo y diagramas de fuerzas internas")
axs[1].plot(x,V,color="#1f77b4"); axs[1].fill_between(x,0,V,alpha=.2); axs[1].set_ylabel("V(y) [N]"); axs[1].set_ylim(0,P*1.25)
axs[1].text(x.mean(),P*1.07,"cortante constante = P",ha="center")
axs[2].plot(x,M/1000,color="#d62728"); axs[2].fill_between(x,0,M/1000,alpha=.2,color="#d62728"); axs[2].set_ylabel("M(y) [N·m]")
axs[2].plot([y_g],[M_g/1000],"o",color="k"); axs[2].annotate(f"galga: M={M_g/1000:.2f} N·m\nσ={sig_a:.2f} MPa",(y_g,M_g/1000),xytext=(y_g+120,M_g/1000*0.75),arrowprops=dict(arrowstyle="->"))
axs[2].text(y_mordaza+3,P*(y_carga-y_mordaza)/1000+0.4,f"M₀={P*(y_carga-y_mordaza)/1000:.2f} N·m (reacción en la mordaza)",va="bottom"); axs[2].set_ylim(0,P*(y_carga-y_mordaza)/1000*1.2)
axs[2].set_xlabel("Posición longitudinal y [mm]"); fig.tight_layout(); fig.savefig(AQUI/"figures"/"fig_diagramas_V_M.png",dpi=200)
print("\nFiguras guardadas en figures/")
