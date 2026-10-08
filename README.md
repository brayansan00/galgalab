# GalgaLab

Entrega final del análisis de una viga tubular de aluminio 1100 instrumentada con una galga extensiométrica. Compara la teoría de Euler–Bernoulli, el ensayo de laboratorio y un modelo de elementos finitos con CalculiX.

**[Leer el informe final](informe/informe_completo.pdf)** · [Fuente LaTeX](informe/informe_completo.tex) · [Resultados de la comparación](datos/resultados_comparacion.json)

Trabajo de **Brayan Smith Espinosa Villegas y Samuel Vanegas Correa**, Universidad Pontificia Bolivariana, Medellín. Elementos Finitos — profesor Elkin Alonso Taborda Espinosa. Informe del **5 de octubre de 2026**.

## Resultados principales

Carga: **49,76613 N** (pesa de 5 kg más herraje de 73 g). Según el informe final, el cero se tomó con la viga montada y antes de colgar el herraje; el peso propio se excluye de la comparación incremental. Sección nominal de 70 × 30 × 1 mm, longitud de 746 mm, carga en y = 711 mm, centro de la galga en y = 205,5 mm y E = 69 GPa.

| Método | Esfuerzo longitudinal σyy | Deformación longitudinal | Diferencia respecto a teoría |
|---|---:|---:|---:|
| Analítico | 11,39852 MPa | 165,19589 µε | Referencia |
| FEM, nodo central, malla de 5 mm | 11,44190 MPa | 166,03622 µε | +0,38061 % en σyy |
| FEM, promedio sobre el área de la galga | 11,44458 MPa | 166,03697 µε | +0,40414 % en σyy |
| Ensayo, descontando la base | 12,54774 MPa (E·ε) | 181,85128 µε | +10,08221 % en E·ε |

El promedio FEM integra la marca CAD de **75 mm²**. El Von Mises central es **11,46408 MPa** y se reporta por separado: la comparación con la galga usa la componente longitudinal. El estudio incluye mallas de 25, 20, 15, 10 y 5 mm, controles de 7 y 4 mm y una variante de apoyo. El máximo global junto a la mordaza depende del refinamiento y de la idealización del apoyo.

El ensayo contiene **7 744 muestras**, a 100 Hz durante 77,43 s. La base de 11–16,5 s es 3,46042 µε; la meseta de 24–53 s es 185,31171 µε. La desviación de 0,85688 µε en la meseta describe dispersión, no la incertidumbre total. La diferencia experimental no permite atribuir una causa única; el informe analiza geometría, instrumentación y montaje.

## Organización

| Carpeta | Contenido |
|---|---|
| [informe/](informe/) | PDF final, fuente LaTeX y figuras utilizadas |
| [codigo/](codigo/) | Análisis de la viga, tratamiento experimental, comparación y figuras |
| [datos/](datos/) | CSV original, hoja de convergencia y resultados JSON |
| [cad/](cad/) | Geometría STEP y modelo nativo Fusion 360 |
| [fem/](fem/) | Generación y extracción FEM; entradas `.inp` y resultados `.frd` |
| [docs/](docs/) | Registro de organización y trazabilidad |
| [archivo/2026-09-30/](archivo/2026-09-30/) | Evidencias y borradores anteriores distintos de la entrega final |

## Reproducir los análisis

Requiere Python 3.10 o posterior. Desde la raíz:

```sh
python -m pip install -r requirements.txt
python codigo/analisis_viga.py
python codigo/analisis_experimental.py
python fem/extraer_galga.py
python codigo/analisis_errores.py
python codigo/figuras.py
python fem/grafica_convergencia.py
python fem/nodos_galga.py
```

Los JSON experimentales, FEM y de comparación se guardan en `datos/`. Los gráficos regenerados se guardan en `codigo/figures/`, `fem/capturas/` o en las rutas indicadas por cada script. El informe conserva sus figuras entregadas. La extracción FEM usa los `.inp` y `.frd` incluidos y no necesita resolver nuevamente el modelo.

Para crear nuevas mallas y resolverlas se necesitan **Gmsh** y **CalculiX**, con `ccx` disponible en el sistema. Para las capturas CAD/FEM se requieren Gmsh, VTK y Pillow. Las dependencias Python opcionales están en [requirements-fem.txt](requirements-fem.txt):

```sh
python -m pip install -r requirements-fem.txt
python fem/fem_calculix.py 25 20 15 10 7 5 4
```

Las nuevas corridas se escriben en `fem/corridas/`. Para compilar el informe en un entorno LaTeX completo, trabajar desde `informe/` y usar `pdflatex informe_completo.tex` dos veces. El PDF entregado se conserva sin modificaciones.

## Trazabilidad

La fuente es **Entrega Viga Galga.zip**. Se conservan el repositorio y todos sus commits anteriores. Se retiraron cinco copias idénticas de la entrega, siete copias anteriores idénticas y ocho marcadores vacíos `.gitkeep`; se ordenaron los resultados FEM de control y se adaptaron las rutas del código. Los archivos anteriores distintos permanecen archivados y no representan la entrega vigente.

La correspondencia y las huellas SHA-256 están en [docs/inventario_entrega.json](docs/inventario_entrega.json). El alcance de las comprobaciones figura en [docs/organizacion_final.md](docs/organizacion_final.md).
