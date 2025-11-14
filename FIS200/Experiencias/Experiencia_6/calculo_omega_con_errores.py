import numpy as np


omega_0 = 10
delta_omega_0 = 2
b = 0.0004835
delta_b = 0.0000001
m = 0.0401
delta_m = 0.00001

# Calcular omega
omega = np.sqrt(omega_0**2 - (b / (2 * m)) ** 2)

# Derivadas parciales
d_omega_d_omega_0 = omega_0 / np.sqrt(omega_0**2 - (b / (2 * m)) ** 2)
d_omega_d_b = -b / (2 * m**2 * np.sqrt(omega_0**2 - (b / (2 * m)) ** 2))
d_omega_d_m = b / (2 * m**3 * np.sqrt(omega_0**2 - (b / (2 * m)) ** 2))

# Propagación de errores
delta_omega = np.sqrt(
    (d_omega_d_omega_0 * delta_omega_0) ** 2
    + (d_omega_d_b * delta_b) ** 2
    + (d_omega_d_m * delta_m) ** 2
)

print(f"Valor de omega: {omega:.4f} rad/s")
print(f"Incertidumbre en omega: {delta_omega:.4f} rad/s")
