# Revisión de GalgaLab

Comparación realizada el 30 de septiembre de 2026 entre `cambios_repo.zip` y `main` de [brayansan00/galgalab](https://github.com/brayansan00/galgalab), commit `dfa231fbb436338dee7460102a4b27766cca2854`.

## Actualización: nuevas exportaciones y lectura local

El usuario aportó nuevos informes de 10 y 15 mm y confirmó que las dos capturas corresponden a Von Mises, en ese orden. La malla nueva de 15 mm tiene **48 735 nodos y 24 301 elementos**, frente a **80 346 y 40 572** de la de 10 mm. Sus máximos globales son 20,722 y 21,018 MPa. La repetición detectada queda limitada al archivo anterior de 15 mm; los nuevos informes sí distinguen las resoluciones.

En el mismo punto (17; 205; 29,997) mm, las capturas dan **10,926 MPa para 15 mm y 10,984 MPa para 10 mm**. La diferencia es 0,058 MPa y la variación respecto a la malla refinada es **0,528 %**. Es una primera evidencia favorable de estabilidad puntual, pendiente de un refinamiento adicional. No es el promedio sobre la rejilla ni la componente σyy.

Ambos HTML nuevos todavía tienen fuerzas de 24,883 N, total vertical 46,764 N, y = 707 mm y gravedad activa. Por tanto, se mantiene la necesidad de reconciliar carga y referencia con el ensayo. Una comprobación nominal de ese caso da σ de flexión ≈ 10,981 MPa por fuerzas más peso de viga, o ≈ 11,019 MPa incorporando también el peso del herraje CAD idealizado. La cercanía apoya la plausibilidad del resultado bajo esa configuración; no constituye equivalencia exacta con Von Mises ni validación del ensayo. Cálculo, supuestos y fuentes están en `fem/mesh_study/actualizacion_2026-09-30/README.md`.

Se conservan los nuevos HTML y capturas originales; la auditoría pasa a nueve informes y las pruebas a ocho. El informe, ZIP y parche se actualizaron con esta evidencia.

## Opinión

Los cambios avanzan el proyecto: añaden el ensayo Samuel–Brayan, un análisis ejecutable, gráficas y una partición útil del CAD. La aritmética analítica y experimental del ZIP es correcta bajo sus hipótesis. **Todavía no es correcto declarar el trabajo validado ni la comparación FEM terminada.** La diferencia de aproximadamente 10–12 % debe explicarse con medidas y configuración verificables, no con porcentajes de incertidumbre supuestos.

## Resultados reproducidos

I = 33 105,33333 mm⁴; c = 15 mm; brazo CAD = 505,5 mm. Con 5,073 kg: P = 49,76613 N, M = 25 156,778715 N·mm, σyy = 11,398516 MPa y εyy = 165,195888 µε. Con solo la pesa de 5 kg: P = 49,05 N, σyy = 11,234493 MPa y εyy = 162,818734 µε.

El CSV tiene 7 744 muestras, 77,43 s y pasos de 0,01 s. La meseta de 24 a 53 s contiene 2 901 muestras; la base de 11 a 16,5 s contiene 551. Meseta = 185,31171 µε; base = 3,46042 µε; incremento = 181,85128 µε. Esfuerzo equivalente uniaxial = 12,547739 MPa. La diferencia es +10,08 % con el herraje añadido después del cero, o +11,69 % si estaba presente al poner en cero. El usuario indicó que no recuerda esa condición.

## Comparación y cambios aplicados

| Área | GitHub / ZIP recibido | Versión revisada |
|---|---|---|
| Ensayo | GitHub solo tenía otro archivo del grupo 1 | Se añade el CSV Samuel–Brayan y se conserva el anterior |
| CAD | Una cara de galga pasa a cuatro | STEP nuevo integrado; siete sólidos válidos, límites y volúmenes conservados; área total 75 mm² |
| Modelo analítico antiguo | `cos(20)` sin conversión, momento con F inclinada, nombres sin definir, extremos manuales | Entradas anteriores remiten al modelo corregido; P resultante, radianes y extremos calculados |
| Procesamiento nuevo | Ventanas fijas, filas descartadas sin diagnóstico, CSV localizado al importar | Ventanas configurables, validación de CSV/tiempos, funciones importables y resultados con SHA-256 |
| Cero experimental | Se asumía que viga sí y herraje no estaban incluidos | Ambos casos conservados y claramente condicionales |
| Esfuerzo | Se llamaba σx pese a eje longitudinal y; superficie libre equiparada a estado uniaxial | σyy; Eεyy condicionado a uniaxialidad; comparación FEM primaria en εyy |
| FEM | Nota del ZIP generalizaba 24,883 N a todas las corridas | Auditoría diferencia 49,05 N, 52,822 N y 46,764 N más gravedad |
| Mallas | Las exportaciones anteriores de 10 y 15 mm repetían resultados | Los HTML nuevos distinguen ambas resoluciones; los anteriores están archivados. La estabilidad puntual no equivale a convergencia definitiva |
| Incertidumbres | Porcentajes de galga, masa y peso propio sin trazabilidad | Se retiran; sensibilidad de espesor calculada y sin confundirla con incertidumbre medida |
| Informe | PDF con afirmaciones pendientes o demasiado fuertes | Fuente revisada; original archivado; conclusiones parciales y condiciones explícitas |

## Observaciones técnicas

**Magnitud FEM.** Una superficie libre en z = 30 mm no impone por sí sola σxx = 0: aún puede existir esfuerzo en el plano y cortante. En elasticidad isotrópica, εyy = [σyy − ν(σxx + σzz)]/E. La lectura más directa es la deformación longitudinal promediada en la rejilla, proyectada en su dirección real. Von Mises máximo del modelo no es la lectura experimental. [COMSOL: esfuerzo plano y ley constitutiva](https://www.comsol.com/blogs/what-is-the-difference-between-plane-stress-and-plane-strain/).

**Fuerzas remotas.** Autodesk permite definir magnitud, componentes, objetivo y punto remoto. Deben revisarse todos: una fuerza remota transfiere los efectos del punto especificado. Para P = 49,76613 N y 20°, la fuerza equivalente es 26,48000 N por lado; para P = 49,05 N, 26,09896 N. El peso del herraje no forma parte física de la tensión de cuerda que sostiene solo la pesa. Distribuirlo con las cuerdas es una equivalencia global y no un modelo local exacto del tornillo. [Autodesk: fuerzas remotas](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/SIM-REMOTE-FORCE-CONCEPT.htm).

**Convergencia.** Las exportaciones originales de 10 y 15 mm se conservan en `fem/mesh_study/historico_2026-09-25/`. Los máximos globales históricos son 17,535 / 20,453 / 21,018 / 21,018 / 20,863 MPa para 25 / 20 / 15 / 10 / 5 mm. El máximo no permite cerrar la convergencia en la galga. Los 80 346 nodos, 40 572 elementos y resúmenes iguales de 10 y 15 mm motivaron la reexportación ya incorporada el 30 de septiembre. El refinamiento nominal es insuficiente para describir la resolución local del espesor de 1 mm.

**Espesor.** Para el escenario de 5,073 kg, t = 0,95 mm da 11,947987 MPa (+4,82 %); t = 1,05 mm da 10,901594 MPa (−4,36 %); t = 0,90 mm da 12,558762 MPa. Esto es sensibilidad del modelo, no prueba de que el espesor sea 0,90 mm. No ajustar el espesor para hacer coincidir el ensayo. Medir también radios de esquina antes de corregir I.

**Cercanía a la mordaza.** La galga está aproximadamente a 63,67 mm del borde CAD. La teoría de viga es una referencia razonable de flexión global, pero los contactos y la restricción local deben comprobarse en FEM; no se afirma uniaxialidad exacta por la distancia o por estar en una cara libre.

**Materiales y masa CAD.** Los HTML usan E = 68 947,20 MPa y todo el herraje como aluminio 1100-O; el análisis usa 69 000 MPa. La diferencia de E es pequeña (0,077 %) y no explica por sí sola el desajuste. El volumen idealizado del herraje no acredita su masa experimental ni el material real.

## Validación realizada y límites

Se reprodujeron los resultados del CSV, la fuerza resultante y los extremos de rejilla; se comprobaron ventanas y errores de datos; se auditaron nueve HTML (incluidos dos anteriores archivados). Pasaron ocho pruebas automáticas. Se reimportaron los dos STEP con Open CASCADE y se verificaron sólidos, volúmenes, límites y caras de galga. Los CSV originales y HTML históricos se conservaron sin modificación. No se ejecutó FEM ni se verificó la configuración activa del `.f3d`.

El PDF de lectura se generó directamente a partir de los resultados verificados y se comprobó visualmente. La fuente LaTeX autónoma se mantiene abierta y editable; no se pudo verificar su compilación porque el editor integrado devolvió `Unable to find standard directories for platform`. El PDF no se presenta como salida de ese compilador.

Falta confirmar la conversión y factor de galga del canal, centro/orientación real de la rejilla, espesor y radios, carga/apoyo reales, contactos, suma de reacciones y convergencia de εyy en la galga. El estado de referencia no se puede reconstruir a partir del CSV solamente.

## Entrega

Se preparó una copia corregida del repositorio y un parche respecto al commit de referencia. La integración conserva las nuevas capturas e informes de 10 y 15 mm publicados en `main`. Los cambios revisados del ZIP se verifican antes de incorporarlos al repositorio mediante la sesión de GitHub del propietario.
