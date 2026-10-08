"""Entrada antigua conservada; ejecuta el modelo revisado sin duplicar ecuaciones."""
from pathlib import Path
import runpy
import sys

if __name__=='__main__':
    source=Path(__file__).resolve().parents[1]/'python'
    sys.path.insert(0,str(source))
    runpy.run_path(str(source/'analytical_model.py'),run_name='__main__')
