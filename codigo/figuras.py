"""Figuras de la Parte 4 a partir de resultados_comparacion.json (ejecutar antes analisis_errores.py)."""
import json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
A = Path(__file__).resolve().parent; (A/'figures').mkdir(exist_ok=True)
R = json.load(open(A.parent/'datos'/'resultados_comparacion.json')); e = R['errores_pct']
fmt = lambda v, d=2: f'{v:.{d}f}'.replace('.', ',')
pct = lambda v: f'{v:+.1f} %'.replace('.', ',')
fig, ax = plt.subplots(figsize=(8.5, 4))
nom = ['Analítico\nσyy = Mc/I', 'FEM σyy\nnodo central', 'FEM σyy\npromedio área galga', 'Ensayo\nE·ε']
val = [R['analitico']['sigma'], R['fem']['syy_centro'], R['fem']['syy_area'], R['ensayo']['sigma_net']]
dif = ['referencia', pct(e['fem_syy_centro_vs_analitico']), pct(e['fem_syy_area_vs_analitico']), pct(e['ensayo_vs_analitico'])]
b = ax.bar(nom, val, color=['#1f4e79', '#2a8f5f', '#7fbf9f', '#d9822b'], width=.6)
ax.set_ylim(10, 13.2); ax.grid(axis='y', alpha=.25)
for r, v, t in zip(b, val, dif): ax.text(r.get_x()+r.get_width()/2, v+.05, fmt(v)+' MPa\n'+t, ha='center', fontsize=9)
ax.set_ylabel('Esfuerzo normal longitudinal [MPa]')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 1)))
ax.set_title('Esfuerzo normal σyy en la galga (P = 49,77 N) y diferencia respecto al analítico', fontsize=10.5)
fig.tight_layout(); fig.savefig(A/'figures'/'fig_comparacion.png', dpi=200); plt.close()

s = R['sens']; items = [('Espesor 1 → 0,95 mm', 't=0,95'), ('Espesor 1 → 0,90 mm', 't=0,90'), ('Altura 30 → 29,5 mm', 'h=29,5'),
                        ('Galga 10 mm hacia la mordaza', 'yg-10'), ('Carga: +1 % de masa', 'm+1%'), ('Brazo de carga +5 mm (yP = 716)', 'yP+5')]
fig, ax = plt.subplots(figsize=(8.5, 3.6))
vals = [s[k]['var_pct'] for _, k in items]
ax.barh([n for n, _ in items][::-1], vals[::-1], color='#2a6f97')
d = e['ensayo_vs_analitico']
ax.axvline(d, color='#d9822b', lw=2, ls='--'); ax.text(d-.2, 5.45, 'Diferencia del ensayo\n(' + pct(d) + ')', color='#d9822b', ha='right', va='top', fontsize=9)
for i, v in enumerate(vals[::-1]): ax.text(v+.15, i, pct(v), va='center', fontsize=9)
ax.set_xlim(0, 12.5); ax.set_xlabel('Aumento del esfuerzo teórico en la galga [%]'); ax.grid(axis='x', alpha=.25)
ax.set_title('Sensibilidad del valor teórico a cambios de ejemplo (no son incertidumbres medidas)', fontsize=10)
fig.tight_layout(); fig.savefig(A/'figures'/'fig_sensibilidad.png', dpi=200); plt.close()
print('ok')
