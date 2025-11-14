import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Leer los datos
data = pd.read_csv("XP4FIS200 V7.txt", delimiter="\t", skiprows=1)

# Convertir las columnas de x, y y t a tipo float, reemplazando la coma por punto
data["t"] = data["t"].str.replace(",", ".").astype(float)
data["x"] = data["x"].str.replace(",", ".").astype(float)
data["y"] = data["y"].str.replace(",", ".").astype(float)

# Posición inicial (primer valor de x y y)
x_0 = data["x"][0]
y_0 = data["y"][0]

# Cálculo del desplazamiento r(t)
data["r(t)"] = np.sqrt((data["x"] - x_0) ** 2 + (data["y"] - y_0) ** 2)

# Calcular r^2(t)
data["r^2(t)"] = data["r(t)"] ** 2

# Calcular el desplazamiento cuadrático medio ⟨r^2(t)⟩
mean_r2 = data["r^2(t)"].mean()

# Calcular la desviación estándar de r^2(t)
std_r2 = data["r^2(t)"].std()

# Calcular el número de observaciones
N = len(data["r^2(t)"])

# Calcular el error estándar
SE = std_r2 / np.sqrt(N)

# Mostrar el desplazamiento cuadrático medio y el error estándar en formato decimal
print(f"Desplazamiento cuadrático medio ⟨r^2(t)⟩: {mean_r2:.8f}")
print(f"Error estándar de ⟨r^2(t)⟩: {SE:.8f}")


def linear_func(t, a, b):
    return a * t + b  # a es la pendiente, b es la ordenada al origen


# Ajustar una línea recta a los datos de r²(t) vs t
popt, pcov = curve_fit(linear_func, data["t"], data["r^2(t)"])

# Extraer la pendiente (a) del ajuste
pendiente = popt[0]
error_pendiente = np.sqrt(np.diag(pcov))[0]


D = pendiente / 4
error_D = error_pendiente / 4


print(f"Coeficiente de difusión D: {D:.8f}")
print(f"Error en el coeficiente de difusión D: {error_D:.8f}")


plt.figure(figsize=(10, 6))


plt.plot(
    data["t"],
    data["r^2(t)"],
    marker="o",
    linestyle="-",
    color="b",
    markersize=4,
    linewidth=3,
    label="⟨r^2(t)⟩",
)


plt.plot(
    data["t"],
    linear_func(data["t"], *popt),
    color="r",
    linestyle="--",
    linewidth=2,
    label="Ajuste lineal",
)


plt.xlabel("(Tiempo ± 0,02)s", fontsize=16, labelpad=10)
plt.ylabel("(r² ± 0.00009)m²", fontsize=16, labelpad=10)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend()


plt.savefig("XP4FIS200 V7.png", dpi=300, bbox_inches="tight")

plt.show()
