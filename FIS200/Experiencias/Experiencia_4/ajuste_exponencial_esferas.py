import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

velocities_config_1 = [0.3464, 0.2516, 0.1077, 0.0884]
velocities_config_2 = [0.4711, 0.2515, 0.1705, 0.1423]
velocities_config_3 = [0.5537, 0.3345, 0.2368, 0.1965]

time = [0, 1, 2, 3]


# Definición de la función exponencial modificada para el ajuste
def modified_exponential_fit(x, a, b, c):
    return a * np.exp(b * x) + c


plt.figure(figsize=(12, 8))

initial_guess_1 = [0.35, -0.5, 0.08]
params_1, _ = curve_fit(
    modified_exponential_fit, time, velocities_config_1, p0=initial_guess_1, maxfev=2000
)
time_fit = np.linspace(0, 3, 100)
velocities_fit_1 = modified_exponential_fit(time_fit, *params_1)
plt.plot(time_fit, velocities_fit_1, color="blue", label="Esfera pequeña")

initial_guess_2 = [0.25, -0.5, 0.05]
params_2, _ = curve_fit(
    modified_exponential_fit, time, velocities_config_2, p0=initial_guess_2, maxfev=2000
)
velocities_fit_2 = modified_exponential_fit(time_fit, *params_2)
plt.plot(time_fit, velocities_fit_2, color="green", label="Esfera mediana")

initial_guess_3 = [0.2, -0.5, 0.02]
params_3, _ = curve_fit(
    modified_exponential_fit, time, velocities_config_3, p0=initial_guess_3, maxfev=2000
)
velocities_fit_3 = modified_exponential_fit(time_fit, *params_3)
plt.plot(time_fit, velocities_fit_3, color="purple", label="Esfera grande")

# Configuración del gráfico
plt.xlabel("(Tiempo ± 0,06) s", fontsize=20)
plt.ylabel("(Velocidad ± 0,001) m/s", fontsize=20)
plt.grid(True)
plt.ylim(0, 0.6)
plt.legend(fontsize=14)

plt.savefig("grafico_ajuste_exponencial.png", dpi=300, transparent=True)

plt.show()
