# GalgaLab

Análisis de una viga tubular de aluminio 1100 con galga extensiométrica. El proyecto compara el cálculo teórico, una medición de laboratorio y una simulación por elementos finitos en CalculiX.

## Entrega final

**[Abrir el informe final en PDF](Informe_GalgaLab.pdf)**

El informe reúne el montaje, el método, los resultados y las conclusiones. Fue presentado el 5 de octubre de 2026 por **Brayan Smith Espinosa Villegas y Samuel Vanegas Correa** en la Universidad Pontificia Bolivariana, Medellín.

## Resultados principales

| Método | Deformación longitudinal en la galga |
| --- | ---: |
| Cálculo teórico | 165,20 µε |
| Simulación FEM, malla de 5 mm | 166,04 µε |
| Medición experimental, descontando la base | 181,85 µε |

La simulación difiere **0,38 %** del esfuerzo teórico en el nodo central. La medición experimental difiere **10,08 %** del valor teórico. El [informe](Informe_GalgaLab.pdf) explica los supuestos, el tratamiento de la señal y las posibles fuentes de diferencia.

## Explorar el proyecto

| Ir a | Contenido |
| --- | --- |
| **[Informe final](Informe_GalgaLab.pdf)** | Documento listo para leer o descargar. |
| [Fuentes y datos](fuentes/README.md) | Código, mediciones, modelo CAD, simulaciones FEM y fuente LaTeX. Incluye instrucciones para reproducir los cálculos. |
| [Histórico](historico/README.md) | Borradores y evidencias previas, conservados como referencia. |

La entrega vigente es el PDF de esta portada junto con los materiales de `fuentes/`. Los archivos de `historico/` documentan etapas anteriores.
