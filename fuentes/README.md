# Fuentes de GalgaLab

Aquí están los materiales que respaldan el [informe final](../Informe_GalgaLab.pdf).

| Carpeta | Contenido |
| --- | --- |
| [informe/](informe/) | Fuente LaTeX y figuras del informe. |
| [datos/](datos/) | Señal experimental original, convergencia y resultados en JSON. |
| [codigo/](codigo/) | Cálculos analíticos, tratamiento experimental y gráficas. |
| [cad/](cad/) | Modelo STEP y archivo nativo de Fusion 360. |
| [fem/](fem/) | Scripts, entradas `.inp` y resultados `.frd` de la simulación. |

## Reproducir los análisis

Con Python 3.10 o posterior, desde la raíz del repositorio:

```sh
python -m pip install -r fuentes/requirements.txt
python fuentes/codigo/analisis_viga.py
python fuentes/codigo/analisis_experimental.py
python fuentes/fem/extraer_galga.py
python fuentes/codigo/analisis_errores.py
python fuentes/codigo/figuras.py
python fuentes/fem/grafica_convergencia.py
python fuentes/fem/nodos_galga.py
```

Los archivos JSON se guardan en `fuentes/datos/`. Las gráficas regeneradas se guardan en `fuentes/codigo/figures/` o en las rutas indicadas por cada script. La extracción FEM lee las entradas y los resultados incluidos; no necesita volver a resolver el modelo.

Para generar nuevas mallas y resolverlas hacen falta Gmsh y CalculiX, con `ccx` disponible en el sistema. Las capturas CAD/FEM también usan VTK y Pillow. Instala las dependencias opcionales y ejecuta:

```sh
python -m pip install -r fuentes/requirements-fem.txt
python fuentes/fem/fem_calculix.py 25 20 15 10 7 5 4
```

Las nuevas corridas se escriben en `fuentes/fem/corridas/`. Para compilar el informe desde la fuente, entra en `fuentes/informe/` y ejecuta `pdflatex informe_completo.tex` dos veces. El [PDF final entregado](../Informe_GalgaLab.pdf) está disponible directamente en la portada.
