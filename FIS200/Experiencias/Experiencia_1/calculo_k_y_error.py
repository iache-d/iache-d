import numpy as np

# Datos iniciales
altura = 0.265  # m
masa = 0.0602  # kg
compresion_resorte = 0.029  # m
gravedad = 9.81  # m/s²
distancia_promedio_m = 50.58 / 100  # Convertir cm a m

# Errores en las mediciones
sigma_m = 0.00001  # kg (0.01 g)
sigma_g = 0.0981  # m/s² (1% de 9.81 m/s²)
sigma_h = 0.0005  # m (0.5 mm)
sigma_c = 0.0005  # m (0.5 mm)


distancias_cm = np.array([50.4, 50.9, 50.5, 50.5, 50.6])  # Distancias en cm
distancias_m = distancias_cm / 100  # Convertir cm a m

# Calcular K para cada distancia
K_values = (masa * gravedad * distancias_m**2) / (2 * altura * compresion_resorte**2)

# Calcular el promedio y la desviación estándar de K
K_mean = np.mean(K_values)
K_std = np.std(K_values, ddof=1)

# Calcular el error de propagación para K
sigma_K = K_mean * np.sqrt(
    (sigma_m / masa) ** 2
    + (sigma_g / gravedad) ** 2
    + (sigma_h / altura) ** 2
    + (2 * sigma_c / compresion_resorte) ** 2
)


print(f"Promedio de K: {K_mean:.2f} N/m")
print(f"Desviación estándar de K: {K_std:.2f} N/m")
print(f"Error de propagación de K: {sigma_K:.2f} N/m")
