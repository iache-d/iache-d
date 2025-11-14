import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


archivos = [
    ("30_grados_lanzamiento1.txt", "Lanzamiento 1"),
    ("30_grados_lanzamiento2.txt", "Lanzamiento 2"),
    ("30_grados_lanzamiento3.txt", "Lanzamiento 3"),
    ("30_grados_lanzamiento4.txt", "Lanzamiento 4"),
    ("30_grados_lanzamiento5.txt", "Lanzamiento 5"),
]


plt.figure(figsize=(12, 8))


x_values = []
y_values = []


for archivo, nombre in archivos:

    df = pd.read_csv(archivo, sep="\s+")

    df["x"] = df["x"].str.replace(",", ".")
    df["y"] = df["y"].str.replace(",", ".")

    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")

    df["y"] = -df["y"]

    # Verificar si hay datos válidos
    if not df["x"].dropna().empty and not df["y"].dropna().empty:

        x_values.extend(df["x"].dropna())
        y_values.extend(df["y"].dropna())

        # Graficar los datos con nombres descriptivos
        plt.plot(df["x"], df["y"], label=nombre, marker="o")
    else:
        print(f"No hay datos válidos en {archivo}.")

# Ajustar los valores para la línea de tendencia promedio
x_values = np.array(x_values)
y_values = np.array(y_values)
coef = np.polyfit(x_values, y_values, 2)
p = np.poly1d(coef)
x_fit = np.linspace(min(x_values), max(x_values), 100)
y_fit = p(x_fit)
plt.plot(x_fit, y_fit, "k--", label="Línea de Tendencia Promedio")

# Datos corregidos para la línea teórica (nuevos puntos)
x_teorico = np.array([3.533239e-2, 0.1422, 0.836])
y_teorico = np.array([-(-3.641431e-1), 0.4055, -(-8.6241788e-2)])


coef_teorico = np.polyfit(x_teorico, y_teorico, 2)
p_teorico = np.poly1d(coef_teorico)
x_teorico_fit = np.linspace(min(x_teorico), max(x_teorico), 100)
y_teorico_fit = p_teorico(x_teorico_fit)


plt.plot(x_teorico_fit, y_teorico_fit, "r--", label="Línea de Tendencia Teórica")

# Verificar si hay datos para graficar
if x_values.size > 0 and y_values.size > 0:

    plt.xlabel("Posición en X ± 0.005 m")
    plt.ylabel("Posición en Y ± 0.005 m")
    plt.legend()
    plt.grid(True)

    plt.xlim(
        left=min(min(x_values), min(x_teorico)) - 0.05,
        right=max(max(x_values), max(x_teorico)) + 0.05,
    )
    plt.ylim(
        bottom=min(min(y_values), min(y_teorico)) - 0.05,
        top=max(max(y_values), max(y_teorico)) + 0.05,
    )

    plt.savefig("grafico_30.png", dpi=300)

    plt.show()
else:
    print("No se encontraron datos válidos para graficar.")
