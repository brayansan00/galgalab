"""Gráfica del estudio de malla en la galga. Lee galga_fem.json (extraer_galga.py) y convergencia.json (número de nodos)."""
import json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
A = Path(__file__).resolve().parent
d = sorted(json.load(open(A.parent/'datos'/'galga_fem.json'))['mallas'], key=lambda r: -r['size'])
s = [r['size'] for r in d]; n = [r['nodos'] for r in d]
vmc = [r['vm_centro'] for r in d]; vma = [r['vm_prom_area'] for r in d]; sya = [r['syy_prom_area'] for r in d]
ana = 11.3985
fmt = lambda v, p: f'{v:.2f}'.replace('.', ',')
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(n, vmc, 'o-', label='Von Mises, nodo central de la galga')
ax[0].plot(n, vma, 's--', label='Von Mises, promedio sobre el área de la galga')
ax[0].plot(n, sya, '^:', color='tab:green', label='σyy, promedio sobre el área de la galga')
ax[0].axhline(ana, color='gray', ls=':', label='Analítico σyy = Mc/I: 11,40 MPa')
for x, y, t in zip(n, vmc, s): ax[0].annotate(f'{t:g} mm', (x, y), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=8)
ax[0].set_xlabel('Número de nodos'); ax[0].set_ylabel('Esfuerzo [MPa]'); ax[0].set_title('Estudio de malla en la galga'); ax[0].grid(alpha=.3); ax[0].legend(fontsize=7.5)
ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(fmt))
ref_c, ref_a = vmc[-1], vma[-1]
ax[1].semilogy(s[:-1], [abs(v-ref_c)/ref_c*100 for v in vmc[:-1]], 'o-', color='tab:red', label='nodo central')
ax[1].semilogy(s[:-1], [abs(v-ref_a)/ref_a*100 for v in vma[:-1]], 's--', color='tab:purple', label='promedio sobre el área')
ax[1].axhline(1, color='gray', ls=':'); ax[1].invert_xaxis(); ax[1].legend(fontsize=8)
ax[1].set_xlabel('Tamaño de elemento [mm]'); ax[1].set_ylabel(f'|VM(h) − VM({s[-1]:g} mm)| / VM({s[-1]:g} mm) [%]'); ax[1].set_title('Variación del Von Mises en la galga'); ax[1].grid(alpha=.3, which='both')
fig.tight_layout(); fig.savefig(A/'fig_convergencia_vm.png', dpi=200)
for r in d: print(f"{r['size']:>4g} mm  nodos {r['nodos']:>7}  VM centro {r['vm_centro']:.3f}  VM área {r['vm_prom_area']:.3f}  syy área {r['syy_prom_area']:.3f}")
