# Integración de la entrega final

Fuente: «Entrega Viga Galga.zip», recibida en la conversación «Organizar repositorio final». Base: commit `fb3930d` de `main`. Organización realizada el 8 de octubre de 2026.

## Cambios

- Se integra el contenido final en `cad/`, `codigo/`, `datos/`, `fem/` e `informe/`.
- Se conserva intacto el PDF entregado y su fuente LaTeX, así como los datos originales, CAD, entradas y resultados FEM.
- Se retiran cinco copias idénticas del ZIP: STEP repetido, dos JSON repetidos, imagen nodal repetida y FRD de 7 mm repetido. La identidad se comprueba con SHA-256.
- Los resultados de control de 4 mm y apoyo extremo de 5 mm se ubican en `fem/frd/`, donde los busca el extractor.
- Se archivan 42 archivos anteriores distintos. Se retiran siete copias anteriores idénticas y ocho marcadores vacíos `.gitkeep`. Git conserva todas las versiones anteriores.
- Se ajustan las rutas de los scripts para compartir CAD y JSON. Se habilita salida UTF-8 en el análisis de la viga para evitar el fallo de impresión de µε en Windows.
- Se mejora el README, se documentan dependencias FEM opcionales y se excluyen las salidas locales regenerables y auxiliares LaTeX.

No se identificaron archivos temporales reales dentro de la entrega que justificaran retirar resultados. Los `.inp` y `.frd`, incluidos los controles de 4 mm y apoyo extremo, se conservan como evidencia reproducible.

## Verificación

Se ejecutaron los siete comandos de análisis publicados en el README: cálculo analítico, tratamiento experimental, extracción FEM, comparación, figuras, convergencia y análisis nodal. Los JSON recalculados coinciden con los entregados, con tolerancia absoluta y relativa de 1e-10; se conservan los archivos entregados para evitar cambios debidos al redondeo de coma flotante.

Se comprobaron la sintaxis de los scripts activos, todos los enlaces locales del README, las figuras referenciadas por LaTeX y la correspondencia del inventario con los archivos conservados. Cada archivo retirado por duplicidad tiene una copia idéntica identificada en `inventario_entrega.json`.

No se ejecutó una nueva solución CalculiX ni se recompiló LaTeX: la extracción se verifica contra los resultados incluidos. La comprobación de trazabilidad conserva el PDF byte por byte; no constituye una auditoría independiente del montaje o de todas las afirmaciones físicas del informe.
