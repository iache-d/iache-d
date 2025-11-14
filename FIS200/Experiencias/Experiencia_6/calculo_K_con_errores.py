import numpy as np

omega_0 = 6.98
delta_omega_0 = 0.001
m = 0.07958
delta_m = 0.00001

K = m * omega_0**2
delta_K = K * np.sqrt((delta_m / m) ** 2 + (2 * delta_omega_0 / omega_0) ** 2)

print(f"Valor de K: {K:.4f} N/m")
print(f"Incertidumbre en K: {delta_K:.4f} N/m")
