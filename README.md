# GalgaLab

Comparación de teoría de vigas, ensayo con galga extensiométrica y FEM de una viga tubular de aluminio 1100. Revisión del ZIP frente a `main` en el commit `dfa231fbb436338dee7460102a4b27766cca2854` (30 de septiembre de 2026).

## Estado y resultados

El cálculo y el tratamiento del CSV son reproducibles. La validación física sigue pendiente: no se recuerda si el herraje de 73 g estaba instalado al poner la galga en cero. Se conservan ambos casos, sin escoger uno como confirmado.

| Referencia experimental | Carga incremental | Teoría en la galga | Diferencia del ensayo respecto a teoría |
|---|---:|---:|---:|
| Herraje añadido después del cero | 49,76613 N | 11,39852 MPa; 165,1959 µε | +10,08 % |
| Herraje presente al poner en cero | 49,05000 N | 11,23449 MPa; 162,8187 µε | +11,69 % |

El ensayo da 185,31171 µε en la meseta; la base previa es 3,46042 µε. El incremento es 181,85128 µε y su esfuerzo equivalente uniaxial es 12,54774 MPa con E = 69 GPa. La desviación de la meseta (0,86 µε) es dispersión de muestras, no incertidumbre total.

Las cifras suponen que el canal exportado ya contiene deformación adimensional y que la rejilla está centrada en la marca CAD y alineada con el eje longitudinal **y**. Falta comprobarlo con el montaje y la configuración de adquisición.

**FEM en revisión.** Las mallas usaron dos fuerzas de 24,883 N en y = 707 mm, con componente vertical conjunta de 46,764 N y gravedad activa. El informe histórico del 24 de septiembre contiene otra configuración: dos fuerzas de 28,106 N y total vertical 52,822 N más gravedad. Las exportaciones anteriores de 10 y 15 mm repetían recuentos y resúmenes; la nueva exportación de 15 mm corrige esa repetición.

**Actualización del 30 de septiembre:** los nuevos informes tienen 80 346 nodos / 40 572 elementos para 10 mm y 48 735 / 24 301 para 15 mm. Las capturas, identificadas como Von Mises por el usuario, dan 10,984 y 10,926 MPa en el mismo punto (17; 205; 29,997) mm: variación de 0,528 % respecto a la malla refinada. Es evidencia de estabilidad puntual entre dos mallas; falta confirmar convergencia con otro refinamiento y comparar la magnitud longitudinal en la rejilla. Véase `fem/mesh_study/actualizacion_2026-09-30/README.md`.

## Reproducir

Desde la raíz del repositorio:

```text
python -m pip install -r requirements.txt
python python/analisis_viga.py
python python/auditar_fem.py
python -m unittest discover -s tests -v
```

El análisis acepta `--csv RUTA`, `--baseline INICIO FIN`, `--plateau INICIO FIN` y `--output-dir CARPETA`. Las ventanas por defecto son inclusivas: base 11–16,5 s (551 muestras), meseta 24–53 s (2 901 muestras). El CSV original conserva 7 744 muestras y 77,43 s a 100 Hz. Se rechazan archivos o ventanas inválidos.

## Archivos

- `python/analisis_viga.py`: modelo, ensayo, sensibilidad de espesor y figuras; `analytical_model.py` conserva la entrada anterior.
- `experimental/raw_data/`: originales; se conservan tanto el archivo previo del grupo 1 como el ensayo Samuel–Brayan. Solo este último alimenta el análisis por defecto.
- `experimental/processed_data/`: señal procesada y resultados JSON, con huella SHA-256 del original.
- `cad/`: STEP actualizado, archivo nativo recibido y verificación geométrica. El archivo Fusion no se ha resuelto ni editado.
- `fem/`: informes vigentes de 10 y 15 mm, exportaciones anteriores conservadas en `mesh_study/historico_2026-09-25/`, auditoría y procedimiento para nuevas corridas.
- `figures/`: gráficas calculadas; `report/informe_viga.tex`: borrador revisado, autónomo con figuras vectoriales incorporadas.
- `report/informe_viga_revisado.pdf`: versión de lectura generada desde los resultados; la compilación LaTeX del editor integrado falló por un problema de entorno y no está verificada.
- `report/original/`: PDF y fuente recibidos, archivados como borrador anterior; no representan la revisión actual.
- `REVISION_CAMBIOS.md`: comparación, opinión y pendientes.

## Para cerrar la validación

Confirmar orientación y centro real de la rejilla, espesor medido, posición de carga y estado de referencia; configurar apoyo y contactos; repetir mallas con la misma carga incremental; comparar **εyy promediada sobre la rejilla** y σyy local, y verificar equilibrio sumando reacciones. Von Mises máximo global no sustituye la lectura de la galga.
