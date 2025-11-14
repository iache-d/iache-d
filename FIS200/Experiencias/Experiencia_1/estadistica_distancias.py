import numpy as np


def calcular_promedio_y_desviacion(values_cm):
    # Convertir valores a metros
    values_m = np.array(values_cm) / 100

    promedio = np.mean(values_m)
    desviacion_std = np.std(
        values_m, ddof=1
    )  # ddof=1 para la desviación estándar muestral

    return promedio, desviacion_std


valores_cm = [50.4, 50.9, 50.5, 50.5, 50.6] #ejemplo de 0 grados


promedio, desviacion_std = calcular_promedio_y_desviacion(valores_cm)


print(f"Promedio de distancia: {promedio:.2f} m")
print(f"Desviación estándar: {desviacion_std:.2f} m")
