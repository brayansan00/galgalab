"""Extrae de los resultados de CalculiX (.frd) el estado en la galga y el máximo global de cada malla.
Salida: galga_fem.json (valor en el nodo central y promedio ponderado por área sobre el parche de la galga). Acepta la estructura de trabajo (corridas/malla_<s>mm_<apoyo>/modelo.*)
o la del paquete (inp/viga_<s>mm.inp, frd/viga_<s>mm.frd)."""
import re, math, json
from pathlib import Path
A = Path(__file__).resolve().parent
E, NU = 69000.0, 0.33
GAL = dict(x0=14.068677, x1=19.068677, y0=198.0, y1=213.0, z=30.0, xc=16.568677, yc=205.5)   # cara de la galga en el STEP (5 x 15 mm)

def rutas(s, apoyo='jaw'):
    wd = A/'corridas'/f'malla_{s:g}mm_{apoyo}'
    if (wd/'modelo.inp').exists(): return wd/'modelo.inp', wd/'modelo.frd'
    suf = '' if apoyo == 'jaw' else f'_{apoyo}'
    return A/'inp'/f'viga_{s:g}mm{suf}.inp', A/'frd'/f'viga_{s:g}mm{suf}.frd'

def leer(fi, ff):
    X = {}
    for l in Path(fi).read_text().split('*ELEMENT')[0].splitlines():
        if re.match(r'^\d+,', l): v = l.split(','); X[int(v[0])] = tuple(map(float, v[1:4]))
    S, en = {}, False
    for ln in open(ff, errors='ignore'):
        if ln.startswith(' -4  STRESS'): en = True; continue
        if en and ln.startswith(' -3'): break
        if en and ln.startswith(' -1'): S[int(ln[3:13])] = [float(ln[13+12*i:25+12*i]) for i in range(6)]
    return X, S

# cuadratura de Dunavant de grado 4 (6 puntos) en coordenadas baricéntricas; pesos suman 1
_A, _B = 0.445948490915965, 0.091576213509771
QP = [((_A, _A, 1-2*_A), 0.223381589678011), ((_A, 1-2*_A, _A), 0.223381589678011), ((1-2*_A, _A, _A), 0.223381589678011),
      ((_B, _B, 1-2*_B), 0.109951743655322), ((_B, 1-2*_B, _B), 0.109951743655322), ((1-2*_B, _B, _B), 0.109951743655322)]
# caras de un C3D10 (orden CalculiX): 3 vértices + 3 nodos intermedios (aristas 01,12,20 / 01,13,30 / 12,23,31 / 02,23,30)
CARAS = [((0,1,2),(4,5,6)), ((0,1,3),(4,8,7)), ((1,2,3),(5,9,8)), ((0,2,3),(6,9,7))]

def leer_elementos(fi):
    txt = Path(fi).read_text(); i = txt.index('*ELEMENT'); els = []
    for l in txt[i:].splitlines()[1:]:
        if l.startswith('*'): break
        v = [int(x) for x in l.split(',')[1:] if x.strip()]
        if len(v) == 10: els.append(v)
    return els

def promedio_area(X, S, els, x0, x1, y0, y1, z=30.0, tol=1e-3):
    """Promedio ponderado por área sobre las caras de la superficie z=const dentro del rectángulo [x0,x1]x[y0,y1].
    Interpola el tensor nodal con las funciones de forma cuadráticas del triángulo de 6 nodos."""
    # una cara pertenece a la galga si sus 6 nodos están en z = const y su centroide cae dentro del rectángulo
    # (la malla es conforme con el contorno de la cara de la galga en el CAD, así que el área total debe ser 75 mm2)
    area = 0.0; acc = dict(syy=0.0, vm=0.0, eps=0.0)
    for e in els:
        for (c, m) in CARAS:
            nodos = [e[k] for k in c] + [e[k] for k in m]
            if not all(abs(X[n][2]-z) < tol for n in nodos): continue
            p = [X[n] for n in nodos[:3]]
            cx, cy = sum(q[0] for q in p)/3, sum(q[1] for q in p)/3
            if not (x0 < cx < x1 and y0 < cy < y1): continue
            ux, uy = (p[1][0]-p[0][0], p[1][1]-p[0][1]), (p[2][0]-p[0][0], p[2][1]-p[0][1])
            A = 0.5*abs(ux[0]*uy[1]-ux[1]*uy[0]); area += A
            for (L, w) in QP:
                N = [L[0]*(2*L[0]-1), L[1]*(2*L[1]-1), L[2]*(2*L[2]-1), 4*L[0]*L[1], 4*L[1]*L[2], 4*L[2]*L[0]]
                sq = [sum(N[k]*S[nodos[k]][j] for k in range(6)) for j in range(6)]
                acc['syy'] += A*w*sq[1]; acc['vm'] += A*w*vm(sq); acc['eps'] += A*w*(sq[1]-NU*(sq[0]+sq[2]))/E*1e6
    return dict(area_mm2=area, **{k: v/area for k, v in acc.items()}) if area > 0 else None

def vm(s):
    a, b, c, d, e, f = s
    return math.sqrt(0.5*((a-b)**2+(b-c)**2+(c-a)**2)+3*(d*d+e*e+f*f))

def analizar(s, apoyo='jaw'):
    fi, ff = rutas(s, apoyo)
    if not Path(ff).exists(): return None
    X, S = leer(fi, ff)
    cen = min(S, key=lambda n: (X[n][0]-GAL['xc'])**2 + (X[n][1]-GAL['yc'])**2 + (X[n][2]-GAL['z'])**2*100)
    sc = S[cen]; sxx, syy, szz = sc[:3]
    parche = [n for n in S if abs(X[n][2]-GAL['z']) < 1e-3 and GAL['x0']-1e-3 <= X[n][0] <= GAL['x1']+1e-3 and GAL['y0']-1e-3 <= X[n][1] <= GAL['y1']+1e-3]
    nmax = max(S, key=lambda n: vm(S[n]))
    pa = promedio_area(X, S, leer_elementos(fi), GAL['x0'], GAL['x1'], GAL['y0'], GAL['y1'])
    return dict(size=s, apoyo=apoyo, nodos=len(X), nodo_centro=cen, xyz_centro=X[cen],
                tensor_centro_MPa=dict(sxx=sxx, syy=syy, szz=szz, sxy=sc[3], syz=sc[4], szx=sc[5]),
                syy_centro=syy, vm_centro=vm(sc), eps_yy_centro_ue=(syy - NU*(sxx+szz))/E*1e6,
                n_parche=len(parche), syy_media_nodal_parche=sum(S[n][1] for n in parche)/len(parche),
                vm_media_nodal_parche=sum(vm(S[n]) for n in parche)/len(parche),
                vm_max_global=vm(S[nmax]), nodo_max=nmax, xyz_max=X[nmax],
                area_galga_mm2=pa['area_mm2'], syy_prom_area=pa['syy'], vm_prom_area=pa['vm'], eps_yy_prom_area_ue=pa['eps'])

if __name__ == '__main__':
    out = [r for r in (analizar(s) for s in (25, 20, 15, 10, 7, 5, 4)) if r]
    alt = analizar(5, 'end')
    json.dump(dict(mallas=out, apoyo_solo_extremo_5mm=alt), open(A.parent/'datos'/'galga_fem.json', 'w'), indent=1)
    for r in out: print(f"{r['size']:>4g} mm  centro: syy {r['syy_centro']:.4f} VM {r['vm_centro']:.4f} eps {r['eps_yy_centro_ue']:.2f} | área {r['area_galga_mm2']:.3f} mm2: syy {r['syy_prom_area']:.4f} VM {r['vm_prom_area']:.4f} eps {r['eps_yy_prom_area_ue']:.2f} | VMmax {r['vm_max_global']:.2f} @ y={r['xyz_max'][1]:.2f}")
    if alt: print('apoyo extremo 5 mm:', round(alt['syy_centro'],4), round(alt['vm_centro'],4))
