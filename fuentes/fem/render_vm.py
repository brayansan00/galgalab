"""Capturas de Von Mises (CalculiX .frd) renderizadas con VTK sin pantalla.
Uso: python render_vm.py [tamano_mm ...]  -> capturas/vm_<tam>mm.png (vista completa + zoom en la galga con malla)"""
import sys, re, math
from pathlib import Path
import numpy as np, vtk
from vtk.util import numpy_support as ns
from PIL import Image, ImageDraw, ImageFont
AQUI = Path(__file__).resolve().parent
GAL = (16.57, 205.5, 30.0)

def rutas(s):
    """Acepta la estructura de trabajo (corridas/malla_<s>mm_jaw/modelo.*) o la del paquete (inp/viga_<s>mm.inp, frd/viga_<s>mm.frd)."""
    wd = AQUI/'corridas'/f'malla_{s:g}mm_jaw'
    if (wd/'modelo.inp').exists(): return wd/'modelo.inp', wd/'modelo.frd'
    return AQUI/'inp'/f'viga_{s:g}mm.inp', AQUI/'frd'/f'viga_{s:g}mm.frd'

def leer(f_inp, f_frd):
    inp = Path(f_inp).read_text().splitlines()
    nodes, elems, mode = {}, [], None
    for ln in inp:
        if ln.startswith('*'):
            mode = 'N' if ln.startswith('*NODE,') and 'NSET=NALL' in ln else ('E' if ln.startswith('*ELEMENT') else None); continue
        if mode == 'N': v = ln.split(','); nodes[int(v[0])] = tuple(map(float, v[1:4]))
        elif mode == 'E': v = ln.split(','); elems.append(tuple(int(i) for i in v[1:11]))   # C3D10 completo (10 nodos)
    S, en = {}, False
    for ln in open(f_frd, errors='ignore'):
        if ln.startswith(' -4  STRESS'): en = True; continue
        if en and ln.startswith(' -3'): break
        if en and ln.startswith(' -1'):
            S[int(ln[3:13])] = [float(ln[13+12*i:25+12*i]) for i in range(6)]
    ids = sorted(nodes); idx = {n: i for i, n in enumerate(ids)}
    X = np.array([nodes[n] for n in ids])
    vmv = np.zeros(len(ids))
    for n, s in S.items():
        a, b, c, d, e, f = s
        vmv[idx[n]] = math.sqrt(0.5*((a-b)**2+(b-c)**2+(c-a)**2)+3*(d*d+e*e+f*f))
    C = np.array([[idx[n] for n in el] for el in elems])
    return X, C, vmv

def aristas_lineales(X, C):
    """Superficie con solo los vértices (para dibujar las aristas reales de los elementos)."""
    g = vtk.vtkUnstructuredGrid(); p = vtk.vtkPoints(); p.SetData(ns.numpy_to_vtk(X, deep=1)); g.SetPoints(p)
    cells = np.hstack([np.full((len(C),1),4), C[:, :4]]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(len(C), ns.numpy_to_vtkIdTypeArray(cells, deep=1)); g.SetCells(vtk.VTK_TETRA, ca)
    sf = vtk.vtkDataSetSurfaceFilter(); sf.SetInputData(g); ed = vtk.vtkExtractEdges(); ed.SetInputConnection(sf.GetOutputPort()); ed.Update()
    return ed.GetOutput()

def grid(X, C, vmv):
    g = vtk.vtkUnstructuredGrid(); p = vtk.vtkPoints(); p.SetData(ns.numpy_to_vtk(X, deep=1)); g.SetPoints(p)
    # Orden de nodos C3D10 de CalculiX = orden de vtkQuadraticTetra (4 vértices + aristas 01,12,20,03,13,23)
    cells = np.hstack([np.full((len(C),1),10), C]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(len(C), ns.numpy_to_vtkIdTypeArray(cells, deep=1))
    g.SetCells(vtk.VTK_QUADRATIC_TETRA, ca)
    s = ns.numpy_to_vtk(vmv, deep=1); s.SetName('VM'); g.GetPointData().SetScalars(s)
    return g

def render(g, rng, edges, cam, size, title, path, clip=None, wire=None):
    surf = vtk.vtkDataSetSurfaceFilter(); surf.SetInputData(g); surf.SetNonlinearSubdivisionLevel(2); surf.Update()
    lut = vtk.vtkLookupTable(); lut.SetNumberOfColors(256); lut.SetHueRange(0.667, 0.0); lut.Build()
    m = vtk.vtkPolyDataMapper(); m.SetInputConnection(surf.GetOutputPort()); m.SetLookupTable(lut); m.SetScalarRange(*rng)
    a = vtk.vtkActor(); a.SetMapper(m)
    ren = vtk.vtkRenderer(); ren.SetBackground(1,1,1); ren.AddActor(a)
    if edges and wire is not None:
        wm = vtk.vtkPolyDataMapper(); wm.SetInputData(wire); wm.ScalarVisibilityOff(); wa = vtk.vtkActor(); wa.SetMapper(wm)
        wa.GetProperty().SetColor(0.1,0.1,0.1); wa.GetProperty().SetLineWidth(0.6); ren.AddActor(wa)
    sb = vtk.vtkScalarBarActor(); sb.SetLookupTable(lut); sb.SetTitle('Von Mises [MPa]'); sb.SetNumberOfLabels(6)
    sb.SetLabelFormat('%.1f'); sb.SetWidth(0.1); sb.SetHeight(0.7); sb.SetPosition(0.88,0.15)
    for t in (sb.GetTitleTextProperty(), sb.GetLabelTextProperty()): t.SetColor(0,0,0); t.SetFontSize(14); t.ShadowOff()
    ren.AddViewProp(sb)
    sp = vtk.vtkSphereSource(); sp.SetCenter(*GAL); sp.SetRadius(cam['marker']); 
    sm = vtk.vtkPolyDataMapper(); sm.SetInputConnection(sp.GetOutputPort()); sa = vtk.vtkActor(); sa.SetMapper(sm); sa.GetProperty().SetColor(0,0,0); ren.AddActor(sa)
    c = ren.GetActiveCamera(); c.SetFocalPoint(*cam['fp']); c.SetPosition(*cam['pos']); c.SetViewUp(*cam['up'])
    if 'scale' in cam: c.SetParallelProjection(1); c.SetParallelScale(cam['scale'])
    else: ren.ResetCamera(); c.Zoom(cam.get('zoom',1))
    ren.ResetCameraClippingRange()
    w = vtk.vtkRenderWindow(); w.SetOffScreenRendering(1); w.SetMultiSamples(0); w.AddRenderer(ren); w.SetSize(*size); w.Render()
    f = vtk.vtkWindowToImageFilter(); f.SetInput(w); f.Update()
    wr = vtk.vtkPNGWriter(); wr.SetFileName(str(path)); wr.SetInputConnection(f.GetOutputPort()); wr.Write()

def componer(a, b, titulo, sub, out):
    A, B = Image.open(a), Image.open(b)
    W = A.width+B.width; H = max(A.height, B.height)+70
    im = Image.new('RGB', (W, H), 'white'); im.paste(A, (0, 70)); im.paste(B, (A.width, 70))
    d = ImageDraw.Draw(im)
    try: fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24); fr = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    except Exception: fb = fr = ImageFont.load_default()
    d.text((15, 8), titulo, fill='black', font=fb); d.text((15, 40), sub, fill='black', font=fr)
    im.save(out)

if __name__ == '__main__':
    tam = [float(a) for a in sys.argv[1:]] or [25, 20, 15, 10, 5]
    import json
    res = {r['size']: r for r in json.load(open(AQUI.parent/'datos'/'convergencia.json'))}
    gal = {r['size']: r for r in json.load(open(AQUI.parent/'datos'/'galga_fem.json'))['mallas']} if (AQUI.parent/'datos'/'galga_fem.json').exists() else {}
    for s in tam:
        X, C, v = leer(*rutas(s)); g = grid(X, C, v); wire = aristas_lineales(X, C)
        ymax = X[int(np.argmax(v)), 1]
        mx = v.max(); r = res[s]
        full = dict(fp=(17,373,15), pos=(900,-700,700), up=(0,0,1), marker=4, zoom=1.45)
        zoom = dict(fp=(17,205,30), pos=(17,205,500), up=(0,1,0), scale=55, marker=1.2)
        t = AQUI/'capturas'
        render(g, (0, mx), False, full, (900, 520), '', t/'_a.png')
        render(g, (0, 14), True, zoom, (700, 520), '', t/'_b.png', wire=wire)
        componer(t/'_a.png', t/'_b.png', f'Malla {s:g} mm  ·  ' + f'{r["nodos"]:,}'.replace(',','.') + ' nodos, ' + f'{r["elementos"]:,}'.replace(',','.') + ' elementos (tetraedros de 2.º orden)',
                 f'Von Mises en el nodo central de la galga: {r["vm_centro"]:.2f} MPa   |   promedio sobre el área de la galga: {gal[s]["vm_prom_area"] if s in gal else r["vm_prom_galga"]:.2f} MPa   |   máx. global (escala izq.): {mx:.1f} MPa en y = {ymax:.0f} mm (borde de la mordaza)', t/f'vm_{s:g}mm.png')
        print(s, mx)
    for n in ('_a.png','_b.png'): (AQUI/'capturas'/n).unlink(missing_ok=True)
