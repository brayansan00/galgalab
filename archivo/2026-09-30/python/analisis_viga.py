"""Teoría y ensayo reproducibles (N, mm, MPa); puesta a cero del herraje desconocida."""
import argparse
import csv
from dataclasses import asdict, dataclass, replace
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Parameters:
    E_MPa: float = 69000.0
    g_m_s2: float = 9.81
    mass_load_kg: float = 5.0
    mass_hardware_kg: float = 0.073
    width_mm: float = 70.0
    height_mm: float = 30.0
    thickness_mm: float = 1.0
    length_mm: float = 746.0
    clamp_y_mm: float = 141.83
    gauge_y_mm: float = 205.5
    grid_length_mm: float = 10.0
    load_y_mm: float = 711.0
    angle_deg: float = 20.0

    def validate(self):
        if not all(math.isfinite(v) for v in asdict(self).values()):
            raise ValueError('Los parámetros deben ser finitos.')
        if min(self.E_MPa,self.g_m_s2,self.mass_load_kg,self.width_mm,self.height_mm,self.thickness_mm,self.grid_length_mm) <= 0:
            raise ValueError('Material, masa y dimensiones deben ser positivos.')
        if self.mass_hardware_kg < 0 or 2*self.thickness_mm >= min(self.width_mm,self.height_mm):
            raise ValueError('Masa de herraje o espesor no válidos.')
        if not (0 <= self.clamp_y_mm < self.gauge_y_mm-self.grid_length_mm/2 < self.gauge_y_mm+self.grid_length_mm/2 < self.load_y_mm <= self.length_mm):
            raise ValueError('La rejilla debe estar entre la mordaza y la carga.')
        if not 0 <= self.angle_deg < 90:
            raise ValueError('Ángulo no válido.')

def analytical(p=Parameters(), include_hardware=True):
    p.validate()
    P=(p.mass_load_kg+(p.mass_hardware_kg if include_hardware else 0))*p.g_m_s2
    b,h,t=p.width_mm,p.height_mm,p.thickness_mm
    I=(b*h**3-(b-2*t)*(h-2*t)**3)/12
    M=P*(p.load_y_mm-p.gauge_y_mm)
    stress=M*(h/2)/I
    F=P/(2*math.cos(math.radians(p.angle_deg)))
    return {'P_N':P,'I_mm4':I,'M_gauge_N_mm':M,'sigma_yy_MPa':stress,
            'epsilon_yy_microstrain':stress/p.E_MPa*1e6,'equivalent_force_per_side_N':F,
            'force_vertical_per_side_N':-P/2,'force_horizontal_abs_per_side_N':F*math.sin(math.radians(p.angle_deg)),
            'sigma_grid_start_MPa':P*(p.load_y_mm-p.gauge_y_mm+p.grid_length_mm/2)*(h/2)/I,
            'sigma_grid_end_MPa':P*(p.load_y_mm-p.gauge_y_mm-p.grid_length_mm/2)*(h/2)/I}

def read_experiment(path):
    timestamps,values=[],[]
    with Path(path).open(encoding='utf-8-sig',newline='') as handle:
        reader=csv.reader(handle,delimiter=';')
        header=next(reader,None)
        if header != ['Time','cDAQ1Mod2/ai0']:
            raise ValueError(f'Cabecera inesperada: {header!r}')
        for line,row in enumerate(reader,2):
            if not row or all(not cell.strip() for cell in row):
                continue
            try:
                if len(row) != 2:
                    raise ValueError('se esperaban dos columnas')
                timestamps.append(datetime.strptime(row[0],'%d/%m/%Y %H:%M:%S.%f'))
                values.append(float(row[1])*1e6)
            except ValueError as exc:
                raise ValueError(f'CSV, línea {line}: {exc}') from exc
    if len(values)<2:
        raise ValueError('El ensayo necesita al menos dos muestras.')
    times=np.array([(ts-timestamps[0]).total_seconds() for ts in timestamps])
    strain=np.asarray(values)
    if not np.all(np.isfinite(strain)) or not np.all(np.diff(times)>0):
        raise ValueError('La señal debe ser finita y los tiempos crecientes.')
    return times,strain

def window_stats(times,strain,bounds):
    start,stop=bounds
    if not (np.isfinite(start) and np.isfinite(stop) and times[0]<=start<stop<=times[-1]):
        raise ValueError(f'Ventana fuera del ensayo: {bounds}')
    data=strain[(times>=start)&(times<=stop)]
    if data.size<2:
        raise ValueError('La ventana necesita al menos dos muestras.')
    return {'start_s':float(start),'end_s':float(stop),'n':int(data.size),
            'mean_microstrain':float(data.mean()),'std_microstrain':float(data.std(ddof=1))}

def experimental(times,strain,p=Parameters(),baseline=(11.0,16.5),plateau=(24.0,53.0)):
    p.validate()
    if baseline[1]>=plateau[0]:
        raise ValueError('La línea base debe preceder a la meseta sin solaparse.')
    base=window_stats(times,strain,baseline)
    flat=window_stats(times,strain,plateau)
    net=flat['mean_microstrain']-base['mean_microstrain']
    dt=np.diff(times)
    return {'samples':len(times),'duration_s':float(times[-1]),'median_sample_rate_Hz':float(1/np.median(dt)),
            'min_step_s':float(dt.min()),'max_step_s':float(dt.max()),'baseline':base,'plateau':flat,
            'net_microstrain':net,'sigma_raw_MPa':flat['mean_microstrain']*p.E_MPa*1e-6,
            'sigma_net_MPa':net*p.E_MPa*1e-6,
            'uncertainty_note':'La desviación de muestras no es la incertidumbre total; no se asume independencia temporal.'}

def figures(times,strain,exp,scenarios,p,folder):
    folder.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.plot(times,strain,lw=.7,label='Deformación registrada')
    for key,color,label in [('baseline','#f89b37','Línea base'),('plateau','#4b995b','Meseta')]:
        s=exp[key]
        ax.axvspan(s['start_s'],s['end_s'],alpha=.18,color=color,label=f"{label}: {s['mean_microstrain']:.2f} µε (n={s['n']})")
    ax.axhline(exp['plateau']['mean_microstrain'],color='#4b995b',ls='--',lw=.8)
    ax.set(xlabel='Tiempo [s]',ylabel='Deformación longitudinal [µε]',title='Ensayo: señal y ventanas de análisis')
    ax.legend(frameon=False,fontsize=8,loc='upper right')
    fig.tight_layout(); fig.savefig(folder/'fig_experimental.png',dpi=200); plt.close(fig)
    # Magnitudes de V y M; su signo depende de la convención de corte.
    y=np.linspace(p.clamp_y_mm,p.length_mm,600)
    fig,axs=plt.subplots(3,1,figsize=(8,7),sharex=True)
    ax=axs[0]
    ax.add_patch(plt.Rectangle((0,-2),p.length_mm,4,fc='#dedede',ec='k'))
    ax.add_patch(plt.Rectangle((0,-5),p.clamp_y_mm,10,fc='#777777',alpha=.5))
    ax.plot(p.gauge_y_mm,2,'s',color='crimson')
    ax.text(p.gauge_y_mm,8,f'Galga: y={p.gauge_y_mm:g} mm',ha='center',color='crimson')
    ax.annotate('P',xy=(p.load_y_mm,-12),xytext=(p.load_y_mm,8),ha='center',arrowprops={'arrowstyle':'->'})
    ax.set(ylim=(-15,15),yticks=[],title='Voladizo: dos escenarios de puesta a cero del herraje')
    for key,label,color in [('hardware_after_zero','73 g añadidos después del cero','#b73535'),('hardware_before_zero','73 g presentes al poner en cero','#28678a')]:
        r=scenarios[key]; P=r['P_N']
        axs[1].plot(y,np.where(y<p.load_y_mm,P,0),color=color,label=f'{label}: P={P:.3f} N')
        axs[2].plot(y,P*np.maximum(p.load_y_mm-y,0)/1000,color=color,label=f"σyy en galga={r['sigma_yy_MPa']:.3f} MPa")
        axs[2].plot(p.gauge_y_mm,r['M_gauge_N_mm']/1000,'o',color=color)
    axs[1].set_ylabel('|V(y)| [N]'); axs[1].legend(fontsize=8,frameon=False)
    axs[2].set(xlabel='Coordenada longitudinal y [mm]',ylabel='|M(y)| [N·m]')
    axs[2].legend(fontsize=8,frameon=False)
    axs[2].axvline(p.gauge_y_mm,ls=':',color='gray',lw=.8)
    fig.tight_layout(); fig.savefig(folder/'fig_diagramas_V_M.png',dpi=200); plt.close(fig)

def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,default=ROOT/'experimental/raw_data/Viga4SamuelBrayan.csv')
    parser.add_argument('--baseline',nargs=2,type=float,default=(11.0,16.5),metavar=('INICIO','FIN'))
    parser.add_argument('--plateau',nargs=2,type=float,default=(24.0,53.0),metavar=('INICIO','FIN'))
    parser.add_argument('--output-dir',type=Path,default=ROOT)
    args=parser.parse_args(argv)
    try:
        times,strain=read_experiment(args.csv); p=Parameters()
        exp=experimental(times,strain,p,tuple(args.baseline),tuple(args.plateau))
    except (OSError,ValueError) as exc:
        parser.error(str(exc))
    scenarios={key:analytical(p,include) for key,include in [('hardware_after_zero',True),('hardware_before_zero',False)]}
    for key,r in scenarios.items():
        r['difference_net_vs_theory_percent']=(exp['sigma_net_MPa']/r['sigma_yy_MPa']-1)*100
        r['difference_raw_vs_theory_percent']=(exp['sigma_raw_MPa']/r['sigma_yy_MPa']-1)*100
        print(f"{key}: P={r['P_N']:.5f} N; σyy={r['sigma_yy_MPa']:.6f} MPa; diferencia={r['difference_net_vs_theory_percent']:+.2f}%")
    print(f"Ensayo: n={exp['samples']}; neto={exp['net_microstrain']:.6f} µε; σ={exp['sigma_net_MPa']:.6f} MPa")
    sensitivity=[]
    for t in [0.90,0.95,1.0,1.05]:
        r=analytical(replace(p,thickness_mm=t))
        sensitivity.append({'thickness_mm':t,'sigma_yy_MPa':r['sigma_yy_MPa'],'change_percent':(r['sigma_yy_MPa']/scenarios['hardware_after_zero']['sigma_yy_MPa']-1)*100})
    report={'parameters':asdict(p),'reference_state':'Herraje al poner a cero: desconocido (confirmado por el usuario).',
            'assumptions':['CSV interpretado como deformación adimensional; falta configuración de adquisición.',
                           'Rejilla longitudinal centrada en la marca CAD: pendiente de comprobar.',
                           'Peso de la viga presente en ambos estados: comparación incremental sin gravedad.',
                           'Fuerzas por lado equivalentes globales; el peso del herraje no es tensión de la cuerda.'],
            'source_file':args.csv.name,'source_sha256':hashlib.sha256(args.csv.read_bytes()).hexdigest(),
            'experimental':exp,'scenarios':scenarios,'thickness_sensitivity':sensitivity}
    processed=args.output_dir/'experimental/processed_data'; processed.mkdir(parents=True,exist_ok=True)
    (processed/'resultados_analisis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (processed/'senal_procesada.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f); writer.writerow(['tiempo_s','epsilon_microstrain','epsilon_menos_base_microstrain'])
        writer.writerows(zip(times,strain,strain-exp['baseline']['mean_microstrain']))
    figures(times,strain,exp,scenarios,p,args.output_dir/'figures')
    print('Estado de referencia y resultado FEM pendientes de confirmar.')
    return report

if __name__=='__main__':
    main()
