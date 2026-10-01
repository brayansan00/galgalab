# Geometría recibida y preparación FEM

Los archivos disponibles son `step/VIGA_FEM.step` y `native/VIGA_FEMa.f3d`. El texto anterior mencionaba un FreeCAD editable y archivos de vista que no están en el repositorio; no se ofrecen como entregables.

## Comparación verificada

Se reimportaron los STEP de GitHub (`dfa231f`) y del ZIP con Open CASCADE. Ambos conjuntos son válidos y contienen siete sólidos. Los volúmenes y límites por sólido coinciden dentro de precisión numérica. La viga ocupa y = 0–746 mm y z = 0–30 mm, con ancho aproximado 70 mm. El borde de división CAD próximo a la mordaza es y = 141,831516 mm; esa división geométrica no confirma por sí sola el apoyo experimental.

La cara de la marca de galga tenía 75 mm² y centro (16,568677; 205,5; 30) mm. El STEP nuevo la divide en cuatro caras de 18,75 mm², manteniendo área y centro ponderado. Es una partición útil para seleccionar el centro. **No garantiza que la rejilla real de 2,5 × 10 mm esté centrada ni que un valor nodal represente su promedio.**

Los valores completos están en `Verificacion_geometria.json`. Esta revisión comprueba validez, volúmenes, límites y caras de galga; no certifica todos los contactos mecánicos ni ejecuta un solver. El `.f3d` se conserva exactamente como fue recibido; su configuración activa no se ha inspeccionado en Fusion.

## Idealizaciones heredadas

Tornillo de diámetro nominal 8 mm, dos arandelas y cierre idealizado, con huecos axiales para la cuerda. La masa medida del herraje es 73 g; no se debe obtener de su volumen idealizado. En las exportaciones antiguas todas las piezas usan aluminio 1100-O, E = 68 947,20 MPa, ν = 0,33 y densidad 2,700 × 10⁻⁶ kg/mm³. Son propiedades de esas corridas, no mediciones nuevas ni confirmación del material real del tornillo. El análisis comparativo adopta E = 69 000 MPa. En el STEP, las propiedades de material no constituyen una definición completa del estudio FEM.

## Carga y referencia

Con g = 9,81 m/s², la pesa aporta 49,05 N y el herraje 0,71613 N. Si estaba presente al poner en cero, este último peso pertenece a la referencia y el incremento experimental es solo 49,05 N. Si se añadió después, el incremento conjunto es 49,76613 N. El usuario no recuerda esta condición: se conservan ambos escenarios.

Dos fuerzas equivalentes simétricas a 20° respecto a vertical valen 26,09896 N por lado para 49,05 N, o 26,48000 N para 49,76613 N. En coordenadas del CAD, Z es vertical y Y longitudinal. Las componentes horizontales se cancelan globalmente. La tensión física de cada cuerda debida a la pesa de 5 kg es 26,09896 N; incluir el peso del herraje en las cuerdas es una simplificación de carga equivalente para flexión global. Para esfuerzos locales, aplicar su peso por separado en la posición real.

Para comparar incrementos elásticos manteniendo los mismos contactos, se puede excluir gravedad y aplicar solo la carga incremental. Otra opción es restar resultados de estado cargado y referencia. No sumar el peso del herraje dos veces. Si cambian contacto o pretensión, justificar el modelo incremental; no suponer superposición sin comprobarla.

## Antes de resolver

Definir zona de mordaza del ensayo, conectar las tres regiones de viga según su continuidad física y justificar contactos tornillo–agujero, arandelas y cierre. Evitar cuerpos libres y uniones automáticas sin fundamento. Comprobar eje del agujero y punto efectivo de carga (CAD: y ≈ 711 mm); documentar qué caras reciben fuerzas remotas y los momentos que estas transfieren. Verificar el equilibrio de la suma de reacciones, la calidad de malla en la pared de 1 mm y la lectura longitudinal en la rejilla.
