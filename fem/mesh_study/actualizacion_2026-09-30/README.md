# Actualización de las mallas de 10 y 15 mm

Se añadieron los dos HTML y las dos capturas originales enviados después de la primera revisión. El usuario identifica la primera captura con 10 mm, la segunda con 15 mm y confirma que la variable seleccionada es **Von Mises**. Las lecturas puntuales proceden de las imágenes; los recuentos, máximos globales y cargas proceden de los HTML. No se ejecutó el solver durante esta revisión.

| Malla | Nodos | Elementos | Von Mises global máximo [MPa] | Von Mises en el punto [MPa] |
|---:|---:|---:|---:|---:|
| 15 mm | 48 735 | 24 301 | 20,722 | 10,926 |
| 10 mm | 80 346 | 40 572 | 21,018 | 10,984 |

Ambas etiquetas señalan (x, y, z) = (17,000; 205,000; 29,997) mm. La diferencia es 0,058 MPa. Respecto a la malla refinada: |10,984 − 10,926| / 10,984 × 100 = **0,5280 %**. Esto indica baja sensibilidad local entre estas dos resoluciones, pero no demuestra por sí solo independencia de malla definitiva. Falta al menos otro refinamiento consistente y la lectura longitudinal/promedio de rejilla que se desea contrastar con el experimento.

La nueva exportación de 15 mm sí tiene recuentos y resultados distintos. La repetición señalada en la revisión inicial pertenece al HTML anterior [15 mm.html](../historico_2026-09-25/15%20mm.html), conservado como historial. El [HTML vigente de 10 mm](../10mm.html) mantiene los recuentos y máximos de su exportación anterior, pero las capturas aportan ahora una lectura local.

## Configuración que todavía debe reconciliarse

Los [informes vigentes de 10 mm](../10mm.html) y [15 mm](../15%20mm.html) conservan dos fuerzas remotas de 24,883 N, componentes Z de −23,382 N por lado, punto remoto y = 707 mm y gravedad 9,807 m/s². Materiales, propiedades, siete contactos fijados y restricción fija Ux/Uy/Uz coinciden en lo exportado. El archivo analizado cambia de `VIGA_FEM v25` a `v26`: esto no acredita identidad geométrica exacta entre versiones.

La fuerza vertical conjunta es 46,764 N, más peso propio. Para el caso incremental definido en el análisis del ensayo aún corresponde revisar P = 49,05 o 49,76613 N, posición y ≈ 711 mm y tratamiento de gravedad según el estado de referencia.

## Comprobación analítica orientativa de la corrida actual

Se usaron los parámetros nominales y las propiedades de estos HTML: área A = 70×30 − 68×28 = 196 mm²; I = 33 105,33333 mm⁴; c = 15 mm; densidad ρ = 2,700×10⁻⁶ kg/mm³; g = 9,807 m/s². El peso lineal nominal es q = Aρg = 0,0051898644 N/mm.

En y = 205 mm, la flexión por las fuerzas exportadas es 46,764×(707−205)×15/I = **10,636743 MPa**. El peso de la viga hasta y = 746 mm aporta q×(746−205)²×15/(2I) = **0,344123 MPa**. La suma aproximada es **10,980866 MPa**, cercana a la lectura de 10,984 MPa.

Si también se incluye el peso del herraje CAD idealizado, su volumen verificado de 6 270,824 mm³ y la densidad exportada dan 16,932 g. Concentrarlo aproximadamente en y = 711 mm añade 0,038069 MPa: total **11,018935 MPa**. La comparación sirve como comprobación orientativa de la configuración actual, no como error certificado ni equivalencia exacta entre Von Mises y esfuerzo longitudinal. Ignora detalles de contacto, hueco y geometría local; los 16,932 g idealizados tampoco sustituyen los 73 g medidos.

El punto mostrado está cerca del centro CAD (16,568677; 205,5; 30) mm, pero no coincide exactamente con él. Ninguna de estas etiquetas es el promedio sobre la rejilla sensible de 2,5×10 mm. Las imágenes originales están en [10mm.png](../10mm.png) y [15mm.png](../15mm.png), y los datos trazables en [lecturas_galga.json](../lecturas_galga.json).
