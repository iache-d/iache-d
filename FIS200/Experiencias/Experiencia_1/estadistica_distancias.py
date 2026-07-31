"""Promedio y desviación estándar de las distancias medidas (lanzamientos a 0°).

Las mediciones viven en `parametros_resorte.py`.
"""

from parametros_resorte import estadistica_distancias

promedio, desviacion_std = estadistica_distancias()

print(f"Promedio de distancia: {promedio:.4f} m")
print(f"Desviación estándar: {desviacion_std:.4f} m")
