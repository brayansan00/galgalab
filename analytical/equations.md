# Modelo analítico preliminar

Unidades: N, mm y MPa. Hipótesis: viga en voladizo, pequeñas deformaciones, elasticidad lineal, sección tubular uniforme lejos del agujero, carga simétrica y galga longitudinal. Confirmar estas condiciones en el ensayo.

## Carga equivalente
P = (5 + 0.073) × 9.81 = 49.76613 N.
Los 73 g corresponden al herraje completo y se cuentan una sola vez. Si se incorpora su peso a P, no se vuelve a añadir por gravedad. El peso propio de la viga se trata aparte.

## Coordenadas y sección
Datos nominales del CAD, pendientes de confirmación experimental:
- Fin de sujeción: Y = 140 mm.
- Centro de la marca superficial de galga: Y = 205.5 mm; no implica que sea el centro confirmado de la rejilla sensible.
- Eje del agujero: Y = 711 mm. En el informe FEM revisado las fuerzas remotas estaban en Y = 707 mm; armonizar ambos modelos.
- Extremo: Y = 746 mm.
- Ancho b = 70 mm, altura vertical h = 30 mm, pared t = 1 mm.
- I = [b h³ − (b−2t)(h−2t)³]/12 = 33105.333 mm⁴.
- c = h/2 = 15 mm.

## Equilibrio y esfuerzo, sin peso propio de viga
a = 711 − 140 = 571 mm.
s_g = 205.5 − 140 = 65.5 mm.
R = P; magnitud del momento de reacción = P a.
|M_g| = P(a−s_g) = 25156.778715 N·mm.
|sigma_g| = |M_g| c / I = 11.3985 MPa.
E = 69000 MPa.
|epsilon_g| = |sigma_g| / E ≈ 165.2 microdeformaciones.
La superficie superior está a tracción para carga vertical descendente en este voladizo.

## Agujero, tornillo y sección variable
La sección neta cambia localmente donde el agujero elimina material de las paredes. El tornillo y las arandelas son cuerpos de transferencia de carga; no se suman al momento de inercia de la viga como si formaran una sección monolítica.
Para el esfuerzo nominal en la galga, alejada del agujero, se emplea I de la sección de la galga y el momento transmitido por la carga. Para la flexión nominal de una viga con sección variable: sigma(s,z) = −M(s) z/I(s). Cerca del agujero esta expresión no captura las concentraciones de tensión ni el contacto.
Para calcular desplazamientos con sección variable, la rigidez E I(s) interviene a lo largo de la viga. El FEM permite resolver la geometría local y los contactos conforme a las hipótesis seleccionadas.
La comparación con galga longitudinal usa esfuerzo/deformación longitudinal; registrar von Mises por separado según el enunciado. No comparar automáticamente el máximo global de von Mises con el esfuerzo nominal en la galga.
