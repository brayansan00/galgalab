# Modelo analítico revisado

El programa vigente es `../python/analisis_viga.py`; `../python/analytical_model.py` permite ejecutar solo el cálculo. La entrada antigua `import math.py` remite al mismo modelo para evitar resultados incompatibles.

`Analicis 1.pdf` se conserva como desarrollo preliminar histórico; no es el informe revisado.

Se usa P·(yP − yg), no la tensión inclinada de una cuerda, para el momento de flexión global. Los ángulos se convierten a radianes. La coordenada longitudinal es y; la magnitud comparada es σyy bajo hipótesis uniaxial. La rejilla de 10 mm, si está centrada, tiene promedio igual al valor central porque el momento es lineal. Sus valores extremos se calculan a partir de las coordenadas y no se introducen manualmente.

El estado de referencia no se recuerda, por lo que se calculan 49,05 y 49,76613 N. La posición real de la rejilla, la orientación del perfil, el espesor, la carga y la aplicabilidad de Euler–Bernoulli cerca de la mordaza siguen sujetos a comprobación.
