# Estudio de malla

Las mallas de **10 y 15 mm** se actualizaron con los informes y capturas exportados el 30 de septiembre de 2026. Los HTML se conservan completos y las capturas mantienen su formato PNG original. Las imágenes anteriores de esas dos mallas se sustituyeron; Git conserva sus versiones previas.

| Malla | Informe de Fusion | Captura | Nodos | Elementos | Von Mises máximo global (MPa) | Von Mises en el punto (MPa) |
|---:|---|---|---:|---:|---:|---:|
| 10 mm | [10mm.html](10mm.html) | [10mm.png](10mm.png) | 80 346 | 40 572 | 21,018 | 10,984 |
| 15 mm | [15 mm.html](15%20mm.html) | [15mm.png](15mm.png) | 48 735 | 24 301 | 20,722 | 10,926 |

Los recuentos y máximos globales proceden de los HTML. Las lecturas puntuales proceden de las etiquetas de las capturas; el autor confirmó que el resultado seleccionado era **Von Mises**. Ambas etiquetas indican (x, y, z) = (17,000; 205,000; 29,997) mm.

La diferencia puntual es 0,058 MPa: **0,5280 %** respecto a la malla de 10 mm. Estos dos resultados muestran baja sensibilidad local al refinamiento, pero todavía no acreditan convergencia definitiva ni equivalencia con la deformación longitudinal medida por la galga. No se ejecutó una nueva simulación para esta actualización.

Ambos HTML exportan dos fuerzas remotas de 24,883 N, con componente Z de −23,382 N por lado, posición remota y = 707 mm y gravedad de 9,807 m/s². El modelo analizado figura como `VIGA_FEM v25` en 10 mm y `VIGA_FEM v26` en 15 mm. Aún debe comprobarse la correspondencia de esta configuración con la carga y el estado de referencia del ensayo.

## Captura de la malla de 10 mm

![Von Mises de la malla de 10 mm: 10,984 MPa en el punto señalado](10mm.png)

## Captura de la malla de 15 mm

![Von Mises de la malla de 15 mm: 10,926 MPa en el punto señalado](15mm.png)

Los archivos de las mallas de 5, 20 y 25 mm corresponden a las exportaciones anteriores.

Los dos HTML anteriores de 10 y 15 mm se conservan en [historico_2026-09-25/](historico_2026-09-25/), con sus recuentos repetidos originales. La comprobación analítica orientativa y el detalle de esta actualización están en [actualizacion_2026-09-30/README.md](actualizacion_2026-09-30/README.md).

## Extracción longitudinal y validación pendientes

1. Fijar geometría, material, referencia, contactos y apoyo; comprobar y ≈ 711 mm y el centro real de la rejilla. Conservar ambos estados del herraje mientras no se confirme la puesta a cero.
2. Para la flexión global incremental, usar P = 49,05 o 49,76613 N. Si se reparte en dos fuerzas equivalentes a 20°, usar 26,09896 o 26,48000 N por lado; documentar objetivos, aplicación y momentos remotos. Excluir cargas ya presentes en la referencia. Véase [LEEME_FEM.md](../../cad/LEEME_FEM.md) para peso del herraje y contacto.
3. Regenerar y resolver cada malla, exportando fecha, nodos, elementos, tamaños efectivos locales y capturas. El tamaño global nominal no demuestra resolución suficiente a través de 1 mm de pared. Justificar sólidos, refinamiento en espesor o un modelo de cascarones.
4. Extraer εyy y σyy en la misma rejilla sensible, preferiblemente promedio espacial ponderado sobre 2,5 × 10 mm; conservar también valor central y tensor local. Si cambia el sistema de coordenadas, proyectar sobre la dirección real de la galga.
5. Comprobar la suma vectorial de reacciones y momentos, más calidad de elementos y ausencia de cuerpos libres. No sumar los máximos de un resumen de reacciones.
6. Calcular variación de la lectura de galga entre refinamientos. Definir el criterio de aceptación antes de interpretar la tabla (p. ej., 2 % si lo permite el curso) y documentar al menos dos refinamientos sucesivos que lo cumplan. Es un criterio propuesto, no una exigencia del profesor ni garantía absoluta de exactitud.

En isotropía lineal, εyy = [σyy − ν(σxx + σzz)]/E. Una superficie libre solo anula las tracciones normales a ella; no obliga a σxx = 0. Comparar directamente εyy evita identificar Eεyy con σyy cuando existen otras componentes. Von Mises puede acompañar el análisis, pero no reemplaza la lectura longitudinal.
