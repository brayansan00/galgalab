import math
#modelo_analitico_viga

#datos entrada

# Modelo analítico de una viga con galga extensiométrica

# Datos de entrada
material = "Aluminio 1100"
E = 69000       # [MPa] Módulo de elasticidad
masa_pesa = 5.0 # [kg]
masa_accesorios = 0.073  # [kg] Tornillo y arandelas
g = 9.807       # [m/s²] Gravedad

ancho_exterior = 70.0   # [mm]
alto_exterior = 30.0    # [mm]
espesor = 1.0           # [mm]
longitud_total = 746.0  # [mm]

posicion_carga = 707.0         # [mm]
inicio_soporte_galga = 198.0   # [mm]
longitud_soporte_galga = 15.0  # [mm]

ancho_rejilla = 2.5     # [mm]
longitud_rejilla = 10.0 # [mm]

# la parte de la  Rejilla sensible que es de 2,5 mm×10 mm
# al estar alineada con el exterior de la galga se puede omitir ya que 
# se alinea con el punto promedio que se toma que es el centro de la galga, 
# por lo que se puede considerar que la carga se aplica en el centro de la galga. 

#desarrollo analítico
masa_total = masa_pesa + masa_accesorios

P = masa_total * g  # [N] Carga aplicada

#Si la carga se representa mediante dos fuerzas simétricas inclinadas 20◦, 
# la magnitud de cada una debe ser:

F = P / (2 * math.cos(math.radians(20)))  # [N] Magnitud de cada fuerza inclinada

# solo se calculan las fuerzas en Y devido a que las Fuerzas en x se cancelan entre sí, 
# por lo que la fuerza resultante es la suma de las fuerzas en Y.

#GEOMETRIA DE LA SECCION TRANSVERSAL DE LA VIGA
# -Sección transversal de la viga (rectángulo hueco)

Bi = ancho_exterior - 2 * espesor  # [mm] Base interior
Hi = alto_exterior - 2 * espesor    # [mm] Altura interior

#MOMENTO DE INERCIA DE LA SECCION TRANSVERSAL DE LA VIGA
I = (ancho_exterior * alto_exterior**3 - Bi * Hi**3) / 12  # [mm^4] Momento de inercia
C = alto_exterior / 2  # [mm] Distancia desde el eje neutro hasta la fibra más alejada

# CORDENADAS DE LA GALGA 

Xg = inicio_soporte_galga + longitud_soporte_galga / 2  # [mm] Coordenada X del centro de la galga

a = posicion_carga - Xg  # [mm] Distancia desde la carga hasta el centro de la galga

M = p * a  # [N·mm] Momento flector en la galga extensiométrica

#Esfuerzo normal por flexión en la galga extensiométrica
sigma = M * C / I  # [MPa] Esfuerzo normal por flexión

#3.7. Deformación longitudinal esperada

epsilon = sigma / E  # [mm/mm] Deformación longitudinal esperada

#3.8 PROMEDIO SOBRE LA REJILLA SENSIBLE

epsilon_i= 11.418 # [MPa]
epsilon_f= 11.192 # [MPa] 

epsilon_promedio = (epsilon_i + epsilon_f) / 2  # [MPa] Promedio de la deformación sobre la rejilla sensible
epsilon_micro = epsilon * 1e6
#imprimir resultados
print("Masa total:", masa_total, "kg")
print("Carga aplicada:", P, "N")
print("Fuerza inclinada por lado:", F, "N")
print("Momento de inercia:", I, "mm^4")
print("Centro de la galga:", Xg, "mm")
print("Brazo de carga:", a, "mm")
print("Momento flector:", M, "N·mm")
print("Esfuerzo normal:", sigma, "MPa")
print("Deformación:", epsilon_micro, "microstrain")
print("Esfuerzo promedio de la rejilla:", sigma_promedio, "MPa")

