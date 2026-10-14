"""Extrae configuración y máximos históricos; no calcula FEM ni convergencia en galga."""
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]

class TableRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows=[]; self.row=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr': self.row=[]
        elif tag in ('td','th'): self.cell=[]
    def handle_data(self,data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:
            if self.row is not None: self.row.append(' '.join(' '.join(self.cell).split()))
            self.cell=None
        elif tag=='tr' and self.row is not None:
            if any(self.row): self.rows.append(self.row)
            self.row=None

def audit(path):
    parser=TableRows(); parser.feed(path.read_text(encoding='utf-8'))
    rows=parser.rows
    def first(label):
        return next((r[1] for r in rows if len(r)==2 and r[0]==label),None)
    loads=[]; current=None
    for row in rows:
        if len(row)==2 and row[0]=='Tipo' and row[1] in ('Gravedad','Fuerza','Fuerza remota'):
            current={'tipo':row[1]}; loads.append(current)
        elif current is not None and len(row)==2 and row[0] in ('Magnitud','Valor X','Valor Y','Valor Z','Posición X','Posición Y','Posición Z'):
            current[row[0]]=row[1]
    def number(value):
        return float(re.match(r'[-+0-9.Ee]+',value.replace('−','-')).group())
    force_z=sum(number(load['Valor Z']) for load in loads if load['tipo']!='Gravedad' and 'Valor Z' in load)
    vm=next((r[-1] for r in rows if r and r[0]=='Von Mises' and len(r)==3),None)
    probe=None
    evidence_path=path.parent/'lecturas_galga.json'
    if evidence_path.exists():
        evidence=json.loads(evidence_path.read_text(encoding='utf-8'))
        source=path.relative_to(ROOT).as_posix()
        for reading in evidence['lecturas']:
            if reading['informe']==source:
                probe={'tipo':evidence['resultado'],'valor_MPa':reading['valor_MPa'],
                       'punto_mm':evidence['punto_mm'],'imagen':reading['imagen'],
                       'origen':evidence['origen'],'alcance':evidence['alcance']}
                break
    return {'archivo':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'tamano_nominal':first('Tamaño medio de elemento (valor absoluto)'),
            'nodos':int(first('Nodos')),'elementos':int(first('Elementos')),
            'orden':first('Orden de elemento'),'E':first('Módulo de Young'),
            'gravedad_activa':any(l['tipo']=='Gravedad' for l in loads),
            'total_fuerzas_Z_N':force_z,'cargas':loads,'VM_max_global':vm,
            'sigma_yy_galga_MPa':None,'epsilon_yy_galga':None,
            'VM_punto_galga_MPa':probe['valor_MPa'] if probe else None,
            'lectura_captura':probe}

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    results=[audit(p) for p in sorted((ROOT/'fem').rglob('*.html'))]
    folder=ROOT/'fem/results'
    (folder/'auditoria_corridas.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['archivo','tamano_nominal','nodos','elementos','orden','E','gravedad_activa','total_fuerzas_Z_N','VM_max_global','VM_punto_galga_MPa','sigma_yy_galga_MPa','epsilon_yy_galga']
    with (folder/'auditoria_corridas.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(results)
    for r in results:
        print(f"{r['archivo']}: nodos={r['nodos']}, elementos={r['elementos']}, Fz={r['total_fuerzas_Z_N']} N, VMmáx={r['VM_max_global']}")
    return results

if __name__=='__main__': main()
