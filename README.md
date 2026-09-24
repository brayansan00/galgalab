# GalgaLab

De la deformación medida al modelo: comparación entre teoría de vigas, cálculo en Python, ensayo con galga extensiométrica y simulación FEM.

## Estado
En desarrollo. El modelo analítico es preliminar; falta confirmar las dimensiones y condiciones del ensayo. Aún no se ha demostrado convergencia de malla ni validación experimental. Python reproducirá el cálculo analítico, no constituye un cuarto método físico independiente.

## Organización
- analytical/: ecuaciones y, cuando estén revisados, cálculos manuales en PDF.
- python/: implementación progresiva del cálculo analítico, tratamiento experimental y convergencia.
- experimental/raw_data/: archivos originales del ensayo, conservados sin modificaciones.
- experimental/processed_data/: datos derivados y registro del procesamiento.
- cad/native/ y cad/step/: modelo editable y geometría de intercambio.
- fem/models/: archivos de configuración de la simulación.
- fem/mesh_study/: tamaños de malla, elementos y resultados en la misma región de galga.
- fem/results/: resultados exportados y configuración de cada corrida.
- figures/: gráficas producidas con datos reales.
- report/: informe final cuando se complete.

## Datos de partida
Aluminio 1100; E = 69 GPa. Tubo nominal de 70 × 30 × 1 mm; longitud total 746 mm. Pesa de 5 kg y herraje completo de 73 g. La geometría simplificada del herraje no reproduce por sí sola su masa medida.

## Pendientes
1. Confirmar orientación, longitud de sujeción, posición/dirección de la rejilla sensible y punto real de carga.
2. Hacer coincidir carga, peso propio y estado de referencia experimental entre teoría y FEM.
3. Revisar contactos y equilibrio de reacciones.
4. Extraer resultados en la galga y demostrar convergencia.
5. Incorporar datos experimentales y documentar incertidumbres.

No se incluyen PDFs finales, gráficas ni programas terminados sin haberlos realizado. Los nombres propuestos para los programas son analytical_model.py, experimental_analysis.py y mesh_convergence.py; se construirán paso a paso.

