import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


Q_agua = np.array(
    [
        1060.61,
        1856.07,
        2386.38,
        2916.68,
        3712.14,
        3977.3,
        4507.6,
        5037.91,
        5568.22,
        6098.52,
        6628.83,
        7159.14,
        7689.44,
        8219.75,
        8749.96,
        9279.36,
        9809.66,
        10339.97,
        10870.28,
        11300.58,
        11730.89,
        12161.19,
        12591.5,
        13021.81,
    ]
)

W_e = np.array(
    [
        599.55,
        1199.1,
        1798.65,
        2398.2,
        2997.75,
        3597.3,
        4196.85,
        4796.4,
        5395.95,
        5995.5,
        6595.05,
        7194.6,
        7794.15,
        8393.7,
        8993.25,
        9592.8,
        10192.35,
        10791.9,
        11391.45,
        11991.0,
        12590.55,
        13190.1,
        13789.65,
        14389.2,
    ]
)

slope, intercept, r_value, p_value, std_err = linregress(Q_agua, W_e)

plt.figure(figsize=(10, 6))
plt.scatter(Q_agua, W_e, color="blue", label="Datos experimentales")

plt.plot(
    Q_agua,
    slope * Q_agua + intercept,
    color="red",
    label=f"Ajuste lineal: $W_e = {slope:.2f} \, Q_{{agua}} + {intercept:.2f}$",
)
residuals = W_e - (slope * Q_agua + intercept)
std_dev = np.std(residuals)

# Configuración del gráfico
plt.xlabel("(Calor absorbido $Q_{agua}$ ± 306) J", fontsize=18)
plt.ylabel("(Trabajo eléctrico $W_e$ ± 205) J", fontsize=18)
plt.tick_params(axis="both", labelsize=12)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig("grafico_trabajo_calor_parte2.png", dpi=300)
plt.show()

error_slope = std_err  # Error de la pendiente
print(f"Equivalente eléctrico del calor (pendiente): {slope:.5f} J/J")
print(f"Error del equivalente eléctrico del calor: {error_slope:.5f} J/J")
print(f"Coeficiente de correlación R²: {r_value**2:.4f}")
