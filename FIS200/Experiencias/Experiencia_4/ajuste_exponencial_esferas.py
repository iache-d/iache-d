import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    "XP5FIS200 BC1.txt",
    "XP5FIS200 BC2.txt",
    "XP5FIS200 BC3.txt",
    "XP5FIS200 BC4.txt",
    "XP5FIS200 BC5.txt",
]

all_data = []
viscosidades = []

for file in files:
    data = pd.read_csv(file, sep="\t", header=1)

    print(f"Columnas en {file}: {data.columns.tolist()}")

    data["t"] = data["t"].str.replace(",", ".").astype(float)
    data["vy"] = data["vy"].str.replace(",", ".").astype(float)

    data.dropna(inplace=True)

    all_data.append(data)

for idx, data in enumerate(all_data):
    plt.plot(data["t"], data["vy"], label=f"Lanzamiento {idx + 1}")

plt.xlabel("(Tiempo ± 0,06) s", fontsize=20)
plt.ylabel("(Velocidad ± 0,001) m/s", fontsize=20)
plt.legend(fontsize=15)
plt.grid()

plt.savefig(f"grafico_final.png", dpi=300)

# Mostrar el gráfico
plt.show()
plt.clf()

# Parámetros
masa_bolita = 0.87e-3  # kg
radio_bolita = 2.525e-3  # m
densidad_medio = 1245  # kg/m³

# Calcular la densidad de la bolita
volumen_bolita = (4 / 3) * np.pi * (radio_bolita**3)  # m³
densidad_bolita = masa_bolita / volumen_bolita  # kg/m³

print(
    f"Densidad de la bolita: {densidad_bolita:.3f} kg/m³"
)  # Verificar densidad de la bolita

# Calcular la velocidad final y viscosidad para cada lanzamiento
velocidades_finales = []
for data in all_data:
    velocidad_final = data["vy"].iloc[-1]  # Velocidad final del último punto
    velocidades_finales.append(velocidad_final)

    # Calcular el coeficiente de viscosidad para cada lanzamiento
    coeficiente_viscosidad = (
        2 / 9 * radio_bolita**2 * (densidad_bolita - densidad_medio) * 9.81
    ) / velocidad_final
    viscosidades.append(coeficiente_viscosidad)

    # Imprimir valores intermedios
    print(
        f"Lanzamiento: Velocidad final = {velocidad_final:.3f} m/s, Viscosidad = {coeficiente_viscosidad:.3f} Pa.s"
    )

velocidad_promedio = np.mean(velocidades_finales)
error_velocidad = np.std(velocidades_finales)

print(f"Velocidades finales promedio: {velocidad_promedio:.3f} m/s")
print(f"Error: {error_velocidad:.3f} m/s")

viscosidad_promedio = np.mean(viscosidades)
error_viscosidad = np.std(viscosidades)

print(f"Viscosidad promedio: {viscosidad_promedio:.3f} Pa.s")
print(f"Error: {error_viscosidad:.3f} Pa.s")

for idx, viscosidad in enumerate(viscosidades):
    print(f"Viscosidad del lanzamiento {idx + 1}: {viscosidad:.3f} Pa.s")

for idx, velocidad in enumerate(velocidades_finales):
    print(f"Velocidad final del lanzamiento {idx + 1}: {velocidad:.3f} m/s")
