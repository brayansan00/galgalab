"""Parte 4: comparación analítico / FEM / ensayo y sensibilidades.
Lee los resultados calculados (no constantes fijas):
  - resultados_exp.json  (Parte 2, analisis_experimental.py)
  - galga_fem.json       (Parte 3, fem/extraer_galga.py)
Busca cada archivo en esta carpeta, en ../datos y en ../fem. Salida: resultados_comparacion.json"""
import json
from pathlib import Path
A = Path(__file__).resolve().parent
def buscar(nombre):
    for d in (A, A.parent/'datos', A.parent/'fem', A.parent/'parte2'):
        if (d/nombre).exists(): return json.load(open(d/nombre))
    raise FileNotFoundError(nombre)

# --- parámetros nominales (los mismos de la Parte 1) ---
g, m_A, E = 9.81, 5.073, 69000.0   # pesa 5 kg + tornillo y arandelas 0,073 kg (la galga se puso en cero sin el herraje)
def sig(t=1.0, h=30.0, b=70.0, P=m_A*g, yP=711.0, yg=205.5):
    I = (b*h**3 - (b-2*t)*(h-2*t)**3)/12
    return P*(yP-yg)*(h/2)/I
def err(a, b): return (a-b)/b*100

exp = buscar('resultados_exp.json'); fem = buscar('galga_fem.json')
f5 = next(r for r in fem['mallas'] if r['size'] == 5)
S_A = sig()
R = dict(
  analitico=dict(sigma=S_A, eps=S_A/E*1e6),
  fem=dict(syy_centro=f5['syy_centro'], vm_centro=f5['vm_centro'], eps_yy_centro=f5['eps_yy_centro_ue'],
           syy_area=f5['syy_prom_area'], vm_area=f5['vm_prom_area'], eps_yy_area=f5['eps_yy_prom_area_ue'], area_mm2=f5['area_galga_mm2']),
  ensayo=dict(eps_net=exp['eps_net'], sigma_net=exp['sigma_net'], sigma_raw=exp['sigma_raw']),
)
R['errores_pct'] = {
  'fem_syy_centro_vs_analitico': err(f5['syy_centro'], S_A), 'fem_syy_area_vs_analitico': err(f5['syy_prom_area'], S_A),
  'fem_vm_centro_vs_analitico': err(f5['vm_centro'], S_A), 'fem_vm_area_vs_analitico': err(f5['vm_prom_area'], S_A),
  'ensayo_vs_analitico': err(exp['sigma_net'], S_A), 'ensayo_sin_base_vs_analitico': err(exp['sigma_raw'], S_A),
  'ensayo_vs_fem_syy_centro': err(exp['sigma_net'], f5['syy_centro']), 'ensayo_vs_fem_syy_area': err(exp['sigma_net'], f5['syy_prom_area']),
  'eps_ensayo_vs_eps_fem_area': err(exp['eps_net'], f5['eps_yy_prom_area_ue']),
}
# sensibilidades del valor teórico (caso A)
casos = {'t=0,95': dict(t=0.95), 't=0,90': dict(t=0.90), 't=1,05': dict(t=1.05), 'h=29,5': dict(h=29.5), 'h=30,5': dict(h=30.5),
         'yg+10': dict(yg=215.5), 'yg-10': dict(yg=195.5), 'yP-5': dict(yP=706), 'yP+5': dict(yP=716),
         'm-1%': dict(P=m_A*g*0.99), 'm+1%': dict(P=m_A*g*1.01)}
R['sens'] = {n: dict(sigma=sig(**kw), var_pct=err(sig(**kw), S_A), dif_vs_exp=err(exp['sigma_net'], sig(**kw))) for n, kw in casos.items()}
# valores que igualarían ensayo y teoría con todo lo demás fijo (sensibilidad matemática, no evidencia)
lo, hi = 0.7, 1.0
for _ in range(60):
    mid = (lo+hi)/2
    if sig(t=mid) > exp['sigma_net']: lo = mid
    else: hi = mid
R['t_que_iguala_mm'] = (lo+hi)/2
R['gf_conf_sobre_real_que_iguala'] = S_A/exp['sigma_net']
# escenario ilustrativo
th = sig(t=0.95, yg=200.5); ex = exp['sigma_net']*0.97
R['escenario'] = dict(teorico=th, ensayo_corregido=ex, dif_pct=err(ex, th))
json.dump(R, open(A.parent/'datos'/'resultados_comparacion.json', 'w'), indent=1)
for k_, v in R['errores_pct'].items(): print(f'{k_:35s} {v:+.3f} %')
print('t que iguala', round(R['t_que_iguala_mm'], 6), ' GFconf/GFreal que iguala', round(R['gf_conf_sobre_real_que_iguala'], 6))
