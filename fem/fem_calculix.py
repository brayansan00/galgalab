"""
FEM de la viga con galga con gmsh + CalculiX (unidades: mm, N, MPa).
Replica el modelo de Fusion: viga + tornillo + 2 arandelas + tuerca (uniones pegadas, malla conforme),
Aluminio 1100 (E=69000 MPa, nu=0.33), 2 fuerzas de 26.48 N a 20 deg de la vertical, sin gravedad.
Uso: python fem_calculix.py [tamano_mm ...]     (por defecto 25 20 15 10 7 5 4; requiere gmsh (Python) y el ejecutable ccx en el PATH)
"""
import sys, os, subprocess, math, json, re, time
from pathlib import Path
import numpy as np, gmsh

AQUI = Path(__file__).resolve().parent
STEP = AQUI.parent / "cad" / "VIGA_FEM.step"
E_, NU = 69000.0, 0.33
P = 5.073 * 9.81
F = P / (2 * math.cos(math.radians(20)))            # 26.48 N por cuerda
FX, FZ = F * math.sin(math.radians(20)), F * math.cos(math.radians(20))
Y_LOAD, Z_LOAD = 711.0, 17.0
X_L, X_R = -21.43, 55.57                            # centros de los huecos entre cabeza/arandela y arandela/tuerca (simétricos respecto a x=17.07)
Y_JAW = 141.83
XMIN, XMAX, ZMIN, ZMAX = -17.93, 52.07, 0.0, 30.0
GAUGE = dict(x0=14.07, x1=19.07, y0=198.0, y1=213.0, z=30.0, xc=16.57, yc=205.5)
EPS = 1e-3

def malla(s, workdir, clamp="jaw"):
    gmsh.initialize(['-nopopup']); gmsh.option.setNumber('General.Terminal', 0)
    gmsh.model.add('viga'); gmsh.model.occ.importShapes(str(STEP)); gmsh.model.occ.synchronize()
    vols = gmsh.model.getEntities(3)
    gmsh.model.occ.fragment(vols, [], removeObject=True, removeTool=True); gmsh.model.occ.synchronize()
    gmsh.option.setNumber('Mesh.MeshSizeMax', s); gmsh.option.setNumber('Mesh.MeshSizeMin', 0.5)
    gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0); gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)
    gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 12)
    gmsh.option.setNumber('Mesh.ElementOrder', 2); gmsh.option.setNumber('Mesh.HighOrderOptimize', 1)
    gmsh.option.setNumber('Mesh.Algorithm3D', 1)
    gmsh.model.mesh.generate(3)
    tags, xyz, _ = gmsh.model.mesh.getNodes()
    xyz = xyz.reshape(-1, 3); idx = {int(t): i for i, t in enumerate(tags)}
    elems = []
    for (dim, tag) in gmsh.model.getEntities(3):
        types, etags, enodes = gmsh.model.mesh.getElements(dim, tag)
        for tp, et, en in zip(types, etags, enodes):
            assert tp == 11, f"tipo de elemento inesperado {tp}"
            en = np.array(en, dtype=int).reshape(-1, 10)
            for row in en: elems.append([row[i] for i in (0,1,2,3,4,5,6,7,9,8)])   # gmsh -> CalculiX C3D10
    nid = {int(t): k+1 for k, t in enumerate(tags)}
    nn, ne = len(tags), len(elems)
    gmsh.finalize()
    X = np.array([xyz[idx[int(t)]] for t in tags])
    # conjuntos de nodos
    def ids(mask): return [int(k)+1 for k in np.where(mask)[0]]
    x, y, z = X[:,0], X[:,1], X[:,2]
    if clamp == "jaw":
        outer = (np.abs(x-XMIN)<EPS)|(np.abs(x-XMAX)<EPS)|(np.abs(z-ZMIN)<EPS)|(np.abs(z-ZMAX)<EPS)
        fix = ids(outer & (y <= Y_JAW+EPS) & (x>=XMIN-EPS) & (x<=XMAX+EPS))
    else:   # solo la cara del extremo y=0
        fix = ids(np.abs(y)<EPS)
    r = np.hypot(y-Y_LOAD, z-Z_LOAD)
    shaft = np.abs(r-4.0) < 5e-3
    gapL = ids(shaft & (x >= -22.93-EPS) & (x <= -19.93+EPS))
    gapR = ids(shaft & (x >= 54.07-EPS) & (x <= 57.07+EPS))
    patch = ids((np.abs(z-GAUGE['z'])<EPS)&(x>=GAUGE['x0']-EPS)&(x<=GAUGE['x1']+EPS)&(y>=GAUGE['y0']-EPS)&(y<=GAUGE['y1']+EPS))
    cen = ids((np.abs(x-GAUGE['xc'])<0.05)&(np.abs(y-GAUGE['yc'])<0.05)&(np.abs(z-GAUGE['z'])<EPS))
    assert fix and gapL and gapR and patch, (len(fix), len(gapL), len(gapR), len(patch))
    inp = workdir / "modelo.inp"
    with open(inp, 'w') as f:
        f.write("*NODE, NSET=NALL\n")
        for k, p in enumerate(X): f.write(f"{k+1},{p[0]:.6f},{p[1]:.6f},{p[2]:.6f}\n")
        f.write(f"*NODE, NSET=RL\n{nn+1},{X_L},{Y_LOAD},{Z_LOAD}\n*NODE, NSET=RR\n{nn+2},{X_R},{Y_LOAD},{Z_LOAD}\n")
        f.write("*ELEMENT, TYPE=C3D10, ELSET=EALL\n")
        for k, el in enumerate(elems): f.write(f"{k+1}," + ",".join(str(nid[int(n)]) for n in el) + "\n")
        def nset(name, lst):
            f.write(f"*NSET, NSET={name}\n")
            for i in range(0, len(lst), 10): f.write(",".join(map(str, lst[i:i+10])) + ",\n")
        nset("FIJO", fix); nset("GAPL", gapL); nset("GAPR", gapR); nset("GALGA", patch)
        if cen: nset("GCEN", cen)
        f.write(f"*MATERIAL, NAME=AL1100\n*ELASTIC\n{E_},{NU}\n*SOLID SECTION, ELSET=EALL, MATERIAL=AL1100\n")
        f.write("*BOUNDARY\nFIJO,1,3\n")
        f.write(f"*RIGID BODY, NSET=GAPL, REF NODE={nn+1}\n")
        f.write(f"*RIGID BODY, NSET=GAPR, REF NODE={nn+2}\n")
        f.write("*STEP\n*STATIC\n*CLOAD\n")
        f.write(f"{nn+1},1,{FX:.6f}\n{nn+1},3,{-FZ:.6f}\n{nn+2},1,{-FX:.6f}\n{nn+2},3,{-FZ:.6f}\n")
        f.write("*NODE FILE\nU\n*EL FILE\nS\n*NODE PRINT, NSET=NALL\nRF\n*END STEP\n")
    return dict(nodos=nn, elementos=ne, fix=len(fix), gap=(len(gapL), len(gapR)), patch=len(patch), cen=cen[0] if cen else None), X

def leer_frd_esfuerzos(frd):
    """Esfuerzos nodales (extrapolados) del .frd ASCII de CalculiX -> dict nodo -> [sxx,syy,szz,sxy,syz,szx]"""
    S = {}; en = False
    for ln in open(frd, errors='ignore'):
        if ln.startswith(' -4  STRESS'): en = True; continue
        if en and ln.startswith(' -3'): break
        if en and ln.startswith(' -1'):
            nid = int(ln[3:13]); vals = [float(ln[13+12*i:25+12*i]) for i in range(6)]; S[nid] = vals
    return S

def vm(s):
    sxx, syy, szz, sxy, syz, szx = s
    return math.sqrt(0.5*((sxx-syy)**2+(syy-szz)**2+(szz-sxx)**2)+3*(sxy**2+syz**2+szx**2))

def correr(s, clamp="jaw"):
    wd = AQUI / "corridas" / f"malla_{s:g}mm_{clamp}"; wd.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); info, X = malla(s, wd, clamp); t1 = time.time()
    r = subprocess.run(["ccx", "-i", "modelo"], cwd=wd, capture_output=True, text=True); t2 = time.time()
    if not (wd/"modelo.frd").exists(): raise RuntimeError(r.stdout[-2000:] + r.stderr[-1000:])
    S = leer_frd_esfuerzos(wd/"modelo.frd")
    # nodos de la galga y centro
    inp = (wd/"modelo.inp").read_text()
    def nset(name):
        m = re.search(rf"\*NSET, NSET={name}\n(.*?)(?=\n\*)", inp, re.S)
        return [int(v) for v in m.group(1).replace("\n","").split(",") if v.strip()] if m else []
    patch, cen = nset("GALGA"), nset("GCEN")
    syy = np.array([S[n][1] for n in patch]); vms = np.array([vm(S[n]) for n in patch])
    res = dict(size=s, clamp=clamp, **info, t_malla=round(t1-t0,1), t_ccx=round(t2-t1,1),
               syy_centro=S[cen[0]][1] if cen else None, vm_centro=vm(S[cen[0]]) if cen else None,
               syy_prom_galga=float(syy.mean()), vm_prom_galga=float(vms.mean()))
    (wd/"resultado.json").write_text(json.dumps(res, indent=1)); return res

if __name__ == "__main__":
    tam = [float(a) for a in sys.argv[1:]] or [25, 20, 15, 10, 7, 5, 4]
    out = []
    for s in tam:
        r = correr(s); out.append(r); print(json.dumps(r), flush=True)
    (AQUI.parent/"datos"/"convergencia.json").write_text(json.dumps(out, indent=1))
