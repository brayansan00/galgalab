# Viga: montaje simplificado para FEM

Archivos: `VIGA_FEM_editable.FCStd` (FreeCAD, primitivas y operaciones editables), `VIGA_FEM.step` (intercambio geométrico), `Vista_montaje.png` y `Verificacion_geometria.json`.

## Geometría conservada

Se importó el STEP suministrado y se conservó íntegro, sin cortar, fusionar ni reconstruir la viga o su galga. El original contiene tres sólidos contiguos. La marca superficial de la galga ocupa 5 × 15 mm, en z = 30 mm, y = 198–213 mm. Se mantiene tal cual; las dimensiones de rejilla sensible de 2,5 × 10 mm citadas en la conversación no se usaron para modificarla.

El agujero existente es de diámetro 8 mm, con eje paralelo a X, situado aproximadamente en y = 711 mm, z = 17 mm. La longitud de la viga es 746 mm.

## Piezas añadidas y supuestos editables

- Tornillo: vástago cilíndrico de diámetro 8 mm, cabeza cilíndrica de diámetro 13 mm y espesor 5,3 mm. Sin rosca helicoidal.
- Dos arandelas, una por cada lateral: diámetro exterior 16 mm, interior 8,4 mm y espesor 2 mm.
- Tuerca de cierre idealizada: anillo de diámetro exterior 13 mm, interior 8 mm y longitud 6,5 mm, sin rosca. Se agregó como supuesto de retención; su presencia y dimensiones deben contrastarse con el montaje real.
- Espacio axial de 3 mm entre la cabeza y la arandela del lado X negativo, y también de 3 mm entre la arandela opuesta y la tuerca de cierre del lado X positivo, para alojar la cuerda por ambos lados. Se alargó el vástago 3 mm para conservar la salida de 2 mm después del cierre. Los espacios son supuestos de modelado, no medidas experimentales. Este montaje no representa una unión pretensada con la cabeza o la tuerca apoyadas en las arandelas.
- El vástago coincide nominalmente con el diámetro del agujero: contacto geométrico sin interferencia ni holgura radial. La cuerda y la pesa no se modelaron.

## Material

Viga, tornillo, ambas arandelas y cierre idealizado: **Aluminio 1100**, **E = 69 GPa = 69 000 MPa = 6,9 × 10¹⁰ Pa**, según la indicación del usuario.

El archivo FreeCAD contiene propiedades por pieza y un objeto de material FEM con referencias a todas las piezas. El STEP se entrega como geometría; no se presupone que el programa de destino reconozca estas propiedades. Reasignar allí el material y E.

No se inventaron coeficiente de Poisson, densidad ni límite elástico. Completar los parámetros necesarios antes de resolver; el archivo no constituye una simulación terminada.

## Masa de 73 g y carga

Los **73 g son la masa experimental indicada de tornillo + arandelas**, guardada como dato de montaje. No se ajustó la densidad ni se alteró la geometría para forzar esa masa. La tuerca añadida es un cierre idealizado; no se dispone de una masa medida aparte y no se añadió una carga adicional por ella. Confirmar su inclusión en el pesaje real.

Con g = 9,81 m/s²:

- Pesa de 5 kg: 49,05 N.
- Masa experimental de 0,073 kg: 0,71613 N.
- Carga equivalente conjunta: **49,76613 N** vertical hacia abajo (−Z si se conserva la orientación del CAD).

Para un análisis estático con fuerza equivalente, incorporar los 0,71613 N una sola vez. No sumar además el peso calculado del herraje mediante gravedad. Si se utiliza gravedad o se requiere inercia dinámica, reconciliar explícitamente la masa geométrica con los 73 g mediante el método de masa adicional/equivalente del programa. El peso propio de la viga es una contribución distinta y depende de cómo se compare con el experimento.

## Preparación del FEM

Definir apoyos según el ensayo, conectividad entre los tres sólidos originales, contacto vástago–agujeros, contacto de arandelas y unión idealizada tuerca–vástago. No dejar cuerpos libres ni unir todas las superficies automáticamente. Eliminar la rosca geométrica requiere representar su función de cierre mediante una condición de unión. Aplicar la carga de la cuerda sobre una zona del vástago en el espacio funcional, evitando una fuerza puntual si interesa el esfuerzo local.

La marca de galga no se convirtió en un sólido nuevo. Seleccionar esa región original para extraer resultados. Faltan malla, contactos, apoyos, cargas activas y resolución; no se ha calculado esfuerzo ni convergencia.

## Comprobación

Se verifican validez geométrica, ausencia de intersecciones volumétricas entre las piezas añadidas y la viga, conservación de caras/áreas/centroides del original y reimportación del STEP con siete sólidos totales (tres originales y cuatro añadidos). El informe JSON contiene los valores obtenidos.
