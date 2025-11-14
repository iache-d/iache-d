import numpy as np

# Definiciones y datos
g = 9.81  # Aceleración debido a la gravedad (m/s^2)
K = 338.96  # Constante de elasticidad (N/m)
sigma_K = 12.187  # Error en la constante de elasticidad (N/m)
compresion_resorte = 0.029  # Compresión del resorte (m)
masa = 0.0602  # Masa (kg)

# Ángulos en grados
angulos = np.array([15, 30, 45])
# Convertir ángulos a radianes
angulos_rad = np.radians(angulos)

# Calcular velocidad inicial
v0 = np.sqrt((2 * K * compresion_resorte**2) / masa)

# Calcular distancias teóricas
distancias_teoricas = (v0**2 * np.sin(2 * angulos_rad)) / g

# Propagación del error
# Distancia teórica en función de K: (v0^2 * sin(2*ángulo)) / g
# Error en distancia teórica se calcula como:
# error_distancia_teorica = abs((d_teorica / K) * sigma_K)
errores_teoricos = np.abs((v0**2 * np.sin(2 * angulos_rad)) / g) * (sigma_K / K)

# Datos experimentales
distancias_experimentales = np.array([0.596, 0.645, 0.648])
errores_experimentales = np.array([0.006, 0.007, 0.006])

# Mostrar los resultados
for angulo, d_teorico, d_error_teorico, d_exp, error_exp in zip(
    angulos,
    distancias_teoricas,
    errores_teoricos,
    distancias_experimentales,
    errores_experimentales,
):
    print(f"Ángulo: {angulo} grados")
    print(f"Distancia Teórica: {d_teorico:.3f} ± {d_error_teorico:.3f} m")
    print(f"Distancia Experimental: {d_exp:.3f} ± {error_exp:.3f} m")
    print()
