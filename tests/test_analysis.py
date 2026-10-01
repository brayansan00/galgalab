import sys
from pathlib import Path
import tempfile
import unittest
from dataclasses import replace
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'python'))
from analisis_viga import Parameters, analytical, read_experiment, experimental, window_stats
from auditar_fem import audit

ROOT=Path(__file__).resolve().parents[1]

class AnalysisTests(unittest.TestCase):
    def test_force_equilibrium_and_two_reference_states(self):
        total=analytical(); incremental=analytical(include_hardware=False)
        self.assertAlmostEqual(total['P_N'],49.76613,places=6)
        self.assertAlmostEqual(incremental['P_N'],49.05,places=6)
        self.assertAlmostEqual(-2*total['force_vertical_per_side_N'],total['P_N'])
        self.assertAlmostEqual(total['sigma_yy_MPa'],11.398516273,places=7)
        self.assertAlmostEqual(incremental['sigma_yy_MPa'],11.234492680,places=7)
    def test_grid_average_matches_center_for_linear_bending(self):
        r=analytical()
        self.assertAlmostEqual((r['sigma_grid_start_MPa']+r['sigma_grid_end_MPa'])/2,r['sigma_yy_MPa'])
    def test_physical_geometry_rejected(self):
        for p in [replace(Parameters(),thickness_mm=20),replace(Parameters(),load_y_mm=190),replace(Parameters(),E_MPa=float('nan'))]:
            with self.assertRaises(ValueError): analytical(p)
    def test_original_experiment_regression(self):
        t,e=read_experiment(ROOT/'experimental/raw_data/Viga4SamuelBrayan.csv')
        result=experimental(t,e)
        self.assertEqual(result['samples'],7744)
        self.assertEqual(result['plateau']['n'],2901)
        self.assertEqual(result['baseline']['n'],551)
        self.assertAlmostEqual(result['sigma_net_MPa'],12.5478,places=3)
        self.assertAlmostEqual(result['duration_s'],77.43,places=2)
    def test_window_errors_are_reported(self):
        t=np.arange(10.0); e=t*0
        for bounds in [(-1,2),(2,20),(5,3),(1.1,1.2)]:
            with self.assertRaises(ValueError): window_stats(t,e,bounds)
        with self.assertRaises(ValueError): experimental(t,e,baseline=(1,4),plateau=(3,8))
    def test_invalid_csv_does_not_silently_drop_samples(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.csv'
            path.write_text('Time;cDAQ1Mod2/ai0\n17/09/2026 17:36:33.099000;0\nincorrecto;1\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'línea 3'): read_experiment(path)
    def test_duplicate_exports_and_loads_detected(self):
        history=ROOT/'fem/mesh_study/historico_2026-09-25'
        a=audit(history/'10mm.html'); b=audit(history/'15 mm.html')
        self.assertEqual((a['nodos'],a['elementos'],a['VM_max_global']),(80346,40572,'21.018 MPa'))
        self.assertEqual((a['nodos'],a['elementos'],a['VM_max_global']),(b['nodos'],b['elementos'],b['VM_max_global']))
        self.assertAlmostEqual(a['total_fuerzas_Z_N'],-46.764,places=3)
        self.assertIsNone(a['sigma_yy_galga_MPa'])
        historic=audit(ROOT/'fem/results/Estudios_Informe_2026-09-24.html')
        self.assertAlmostEqual(historic['total_fuerzas_Z_N'],-52.822,places=3)
    def test_updated_meshes_and_probe_quantity(self):
        folder=ROOT/'fem/mesh_study'
        fine=audit(folder/'10mm.html'); coarse=audit(folder/'15 mm.html')
        self.assertEqual((fine['nodos'],fine['elementos']),(80346,40572))
        self.assertEqual((coarse['nodos'],coarse['elementos']),(48735,24301))
        self.assertEqual(fine['VM_punto_galga_MPa'],10.984)
        self.assertEqual(coarse['VM_punto_galga_MPa'],10.926)
        self.assertEqual(fine['lectura_captura']['tipo'],'Von Mises')
        self.assertEqual(fine['lectura_captura']['punto_mm'],coarse['lectura_captura']['punto_mm'])
        self.assertIsNone(fine['sigma_yy_galga_MPa'])
        self.assertIsNone(coarse['epsilon_yy_galga'])
        change=abs(fine['VM_punto_galga_MPa']-coarse['VM_punto_galga_MPa'])/fine['VM_punto_galga_MPa']*100
        self.assertAlmostEqual(change,0.5280407866,places=8)

if __name__=='__main__': unittest.main()
