# Corridas históricas: configuraciones distintas

Los HTML históricos se conservan sin cambios. Las exportaciones anteriores de 10 y 15 mm están en `../mesh_study/historico_2026-09-25/`; los HTML vigentes de esas mallas están en `../mesh_study/`. La auditoría de `python/auditar_fem.py` produce `auditoria_corridas.csv` y `.json`, con huellas de los originales y campos longitudinales de galga vacíos porque no están exportados.

La actualización del 30 de septiembre incorpora dos HTML vigentes y capturas en `../mesh_study/`: se auditan nueve informes en total, incluidos los dos HTML anteriores archivados. Su comparación se documenta en `../mesh_study/actualizacion_2026-09-30/README.md`. La columna `VM_punto_galga_MPa` incorpora las lecturas de las capturas con su procedencia; `sigma_yy_galga_MPa` y `epsilon_yy_galga` permanecen vacías, porque Von Mises no es esa componente ni una deformación. El nuevo informe de 15 mm resuelve la repetición de recuentos anterior.

| Archivo o conjunto | Fuerzas aplicadas | Total vertical de fuerzas | Gravedad |
|---|---|---:|---|
| Informe 2026-09-23 | Una fuerza vertical de 49,05 N | −49,05 N | 9,807 m/s² |
| Informe 2026-09-24 | Dos fuerzas de 28,106 N | −52,822 N | 9,807 m/s² |
| Cinco mallas originales; dos HTML en `historico_2026-09-25/` | Dos fuerzas de 24,883 N, y = 707 mm | −46,764 N | 9,807 m/s² |

La nota del ZIP que atribuye 24,883 N a todas las corridas era incorrecta. Las componentes exportadas tienen redondeo: la recomposición trigonométrica de las mallas da 46,76474 N. El total de cada fila no incluye peso propio.

Los máximos globales de Von Mises no son lecturas de galga. El resumen de reacciones contiene extremos, no la suma de reacciones de apoyo; no permite verificar por sí solo el equilibrio global.

No se han recalculado estos estudios ni certificado sus contactos. Véase `../mesh_study/README.md` para completar la validación.
