"""Nodos de la cara de la galga (malla de 5 mm): valores nodales, tabla CSV y figura. Usa los .inp/.frd del paquete."""
import csv, json, sys, math
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import extraer_galga as G
A = Path(__file__).resolve().parent
size = float(sys.argv[1]) if len(sys.argv) > 1 else 5
fi, ff = G.rutas(size); X, S = G.leer(fi, ff); els = G.leer_elementos(fi)
g = G.GAL; tol = 1e-3
# triángulos (vértices) de la cara de la galga
tris, nodos = [], set()
for e in els:
    for c, m in G.CARAS:
        ns = [e[k] for k in c] + [e[k] for k in m]
        if not all(abs(X[n][2]-g['z']) < tol for n in ns): continue
        p = [X[n] for n in ns[:3]]; cx = sum(q[0] for q in p)/3; cy = sum(q[1] for q in p)/3
        if g['x0'] < cx < g['x1'] and g['y0'] < cy < g['y1']: tris.append(ns); nodos.update(ns)
nodos = sorted(nodos, key=lambda n: (round(X[n][1], 3), X[n][0]))
cen = min(nodos, key=lambda n: (X[n][0]-g['xc'])**2+(X[n][1]-g['yc'])**2)
vert = {n for t in tris for n in t[:3]}
rows = []
for n in nodos:
    s = S[n]; rows.append(dict(nodo=n, tipo='vértice' if n in vert else 'intermedio', x=X[n][0], y=X[n][1], z=X[n][2],
        sxx=s[0], syy=s[1], szz=s[2], txy=s[3], vm=G.vm(s), eps_yy_ue=(s[1]-G.NU*(s[0]+s[2]))/G.E*1e6, centro=int(n == cen)))
with open(A/f'nodos_galga_{size:g}mm.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';'); w.writeheader()
    for r in rows: w.writerow({k: (f'{v:.4f}'.replace('.', ',') if isinstance(v, float) else v) for k, v in r.items()})
sy = np.array([r['syy'] for r in rows]); vmv = np.array([r['vm'] for r in rows])
res = dict(size=size, n_nodos=len(rows), n_vertices=len(vert), n_triangulos=len(tris), nodo_central=cen,
           syy_media_nodal=float(sy.mean()), syy_min=float(sy.min()), syy_max=float(sy.max()),
           vm_media_nodal=float(vmv.mean()), vm_min=float(vmv.min()), vm_max=float(vmv.max()),
           **{'promedio_area': G.promedio_area(X, S, els, g['x0'], g['x1'], g['y0'], g['y1'])})
json.dump(res, open(A/f'nodos_galga_{size:g}mm.json', 'w'), indent=1); print(json.dumps(res, indent=1))
# --- figura
xs = np.array([r['x'] for r in rows]) - g['x0']; ys = np.array([r['y'] for r in rows]); idx = {n: i for i, n in enumerate(nodos)}
T = np.array([[idx[a], idx[b], idx[c]] for a, b, c, *_ in tris]); tri = Triangulation(xs, ys, T)
fig, ax = plt.subplots(1, 2, figsize=(10.5, 6.8), gridspec_kw=dict(width_ratios=[1, 1.25]))
a = ax[0]; a.set_aspect('equal'); tc = a.tripcolor(tri, sy, shading='gouraud', cmap='viridis')
a.triplot(tri, color='k', lw=.6); a.plot(xs, ys, 'o', ms=3.2, color='w', mec='k', mew=.5)
ic = idx[cen]; a.plot(xs[ic], ys[ic], 's', ms=8, color='red', mec='k', label=f'nodo central ({sy[ic]:.2f} MPa)')
a.set_xlim(-.3, 5.3); a.set_ylim(g['y0']-.5, g['y1']+.5); a.set_xlabel('x respecto al borde de la galga [mm]'); a.set_ylabel('y [mm]')
a.set_title(f'Cara de la galga, malla {size:g} mm\n{len(rows)} nodos ({len(vert)} vértices), {len(tris)} triángulos', fontsize=10)
cb = fig.colorbar(tc, ax=a, orientation='horizontal', pad=.14, fraction=.04); cb.set_label('σyy [MPa]'); a.legend(fontsize=8, loc='upper center', bbox_to_anchor=(.5, -.42), frameon=False)
b = ax[1]; b.scatter(ys, sy, s=14, c='#1f4e79', label='σyy en cada nodo de la galga'); b.plot(ys[ic], sy[ic], 's', ms=8, color='red', mec='k', label='nodo central')
yy = np.linspace(g['y0'], g['y1'], 50); P = 5.073*9.81; I = (70*30**3-68*28**3)/12
b.plot(yy, P*(711-yy)*15/I, color='#d9822b', lw=1.8, label='analítico Mc/I (lineal en y)')
b.axhline(res['promedio_area']['syy'], color='#2a8f5f', ls='--', label=f"promedio sobre el área = {res['promedio_area']['syy']:.2f} MPa")
b.set_xlabel('y [mm]'); b.set_ylabel('σyy [MPa]'); b.grid(alpha=.25); b.legend(fontsize=8, frameon=False)
b.set_title(f'σyy nodal: {sy.min():.2f} a {sy.max():.2f} MPa; media nodal {sy.mean():.2f} MPa', fontsize=10)
fig.tight_layout(); fig.savefig(A/f'fig_nodos_galga_{size:g}mm.png', dpi=200); print('ok')
