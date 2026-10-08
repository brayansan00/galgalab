"""Imagenes del modelo CAD (STEP) con VTK sin pantalla: vista general, detalle de carga y detalle de galga."""
import numpy as np, gmsh, vtk
from vtk.util import numpy_support as ns
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
A = Path(__file__).resolve().parent; OUT = A/'capturas'; OUT.mkdir(exist_ok=True)
gmsh.initialize(['-nopopup']); gmsh.option.setNumber('General.Terminal', 0)
gmsh.model.add('v'); gmsh.model.occ.importShapes(str(A.parent/'cad'/'VIGA_FEM.step')); gmsh.model.occ.synchronize()
gmsh.option.setNumber('Mesh.MeshSizeMax', 4); gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 20)
gmsh.model.mesh.generate(2)
COL = {1:(0.62,0.72,0.85), 2:(0.45,0.58,0.78), 3:(0.62,0.72,0.85), 4:(0.35,0.35,0.38), 5:(0.85,0.55,0.25), 6:(0.85,0.55,0.25), 7:(0.30,0.65,0.45)}
NAM = {1:'Viga (tramo 140–141,83 mm)',2:'Viga (tramo en mordaza 0–140 mm)',3:'Viga (tramo libre)',4:'Tornillo',5:'Arandela',6:'Arandela',7:'Tuerca'}
GAUGE = (14.07,19.07,198.0,213.0,30.0)
pts_all, tris_all, cols_all = [], [], []
n0 = 0
for d, v in gmsh.model.getEntities(3):
    for fd, ft in gmsh.model.getBoundary([(d, v)], oriented=False):
        t, xyz, _ = gmsh.model.mesh.getNodes(2, abs(ft), includeBoundary=True)
        et, ets, en = gmsh.model.mesh.getElements(2, abs(ft))
        X = xyz.reshape(-1, 3); idx = {int(k): i for i, k in enumerate(t)}
        T = np.array([[idx[int(k)] for k in row] for row in np.array(en[0]).reshape(-1, 3)])
        c = np.array(COL[v])
        bb = gmsh.model.getBoundingBox(2, abs(ft))
        if v == 3 and abs(bb[2]-30) < 1e-3 and abs(bb[5]-30) < 1e-3 and bb[0] >= GAUGE[0]-.01 and bb[3] <= GAUGE[1]+.01 and bb[1] >= GAUGE[2]-.01 and bb[4] <= GAUGE[3]+.01: c = np.array((0.95, 0.75, 0.1))
        pts_all.append(X); tris_all.append(T+n0); cols_all.append(np.tile(c, (len(T), 1))); n0 += len(X)
gmsh.finalize()
P = np.vstack(pts_all); T = np.vstack(tris_all); C = (np.vstack(cols_all)*255).astype(np.uint8)
pd = vtk.vtkPolyData(); p = vtk.vtkPoints(); p.SetData(ns.numpy_to_vtk(P, deep=1)); pd.SetPoints(p)
ca = vtk.vtkCellArray(); ca.SetCells(len(T), ns.numpy_to_vtkIdTypeArray(np.hstack([np.full((len(T),1),3), T]).astype(np.int64).ravel(), deep=1)); pd.SetPolys(ca)
col = ns.numpy_to_vtk(C, deep=1); col.SetName('c'); pd.GetCellData().SetScalars(col)
nrm = vtk.vtkPolyDataNormals(); nrm.SetInputData(pd); nrm.ComputePointNormalsOff(); nrm.ComputeCellNormalsOn(); nrm.Update()

def shot(path, pos, fp, up, scale=None, size=(900, 520), edges=False):
    m = vtk.vtkPolyDataMapper(); m.SetInputConnection(nrm.GetOutputPort()); m.SetScalarModeToUseCellData(); m.SetColorModeToDirectScalars()
    a = vtk.vtkActor(); a.SetMapper(m)
    if edges: a.GetProperty().EdgeVisibilityOn(); a.GetProperty().SetEdgeColor(0.25,0.25,0.25); a.GetProperty().SetLineWidth(0.4)
    ren = vtk.vtkRenderer(); ren.SetBackground(1,1,1); ren.AddActor(a)
    c = ren.GetActiveCamera(); c.SetFocalPoint(*fp); c.SetPosition(*pos); c.SetViewUp(*up)
    if scale: c.SetParallelProjection(1); c.SetParallelScale(scale)
    else: ren.ResetCamera(); c.Zoom(1.7)
    ren.ResetCameraClippingRange()
    w = vtk.vtkRenderWindow(); w.SetOffScreenRendering(1); w.SetMultiSamples(0); w.AddRenderer(ren); w.SetSize(*size); w.Render()
    f = vtk.vtkWindowToImageFilter(); f.SetInput(w); f.Update()
    wr = vtk.vtkPNGWriter(); wr.SetFileName(str(path)); wr.SetInputConnection(f.GetOutputPort()); wr.Write()

shot(OUT/'cad_general.png', (1000,-650,650), (17,373,15), (0,0,1))
shot(OUT/'cad_carga.png', (330,1000,330), (17,711,15), (0,0,1), scale=45, size=(900,520))
shot(OUT/'cad_galga.png', (17,205,600), (17,205,30), (0,1,0), scale=22, size=(520,520))
print('ok')

# leyenda
def leyenda(path, items):
    im = Image.open(path).convert('RGB'); d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    except Exception: f = ImageFont.load_default()
    y = 12
    for c, t in items:
        d.rectangle([12, y, 30, y+14], fill=tuple(int(255*v) for v in c), outline='black'); d.text((38, y-1), t, fill='black', font=f); y += 22
    im.save(path)
leyenda(OUT/'cad_general.png', [((0.62,0.72,0.85),'Viga de aluminio 1100 (70×30×1 mm)'), ((0.45,0.58,0.78),'Tramo sujeto por la mordaza'), ((0.95,0.75,0.1),'Marca de la galga (5×15 mm)'), ((0.35,0.35,0.38),'Tornillo'), ((0.85,0.55,0.25),'Arandelas'), ((0.30,0.65,0.45),'Tuerca idealizada')])
leyenda(OUT/'cad_galga.png', [((0.95,0.75,0.1),'Marca de la galga')])
