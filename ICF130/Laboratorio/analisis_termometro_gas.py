import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Datos experimentales
# Temperatura real (°C) ±1°C
T_real = np.array([2,10,20,30,40,50,60,70,80,90,96])
dT_real = 1

# Resistencia PT100 (Ω) ±0.1Ω
R_pt100 = np.array([100.6,104,107.7,111.4,115.3,118.9,122,126.6,129.8,133.3,135.7])
dR = 0.1

# Altura mercurio (cm) ±0.05cm
h_mercurio = np.array([26.65,26.4,26.15,25.85,25.5,25,24.75,24.4,23.8,23.3,23.05])
dh = 0.05

# Parámetros
rho = 13.6e3      # kg/m³ densidad del mercurio
g = 9.81          # m/s²
Patm = 94990      # Pa (presión atmosférica medida: 949.90 hPa)

# Convertir altura de cm a m
h_m = h_mercurio / 100

# Cálculo de presión del bulbo
# Se toma la diferencia de alturas con respecto a la primera medición
delta_h = h_m - h_m[0]  # cambio de altura relativo al inicio
P_gas = Patm - rho * g * delta_h  # signo negativo: menor altura → menor presión

# Ajuste lineal PT100
slope, intercept, r_value, p_value, std_err = linregress(T_real, R_pt100)
R0 = intercept
alpha = slope / intercept

# Incertidumbre del intercepto
n = len(T_real)
sigma_intercept = std_err * np.sqrt(np.sum(T_real**2)/n)

# Propagación de error para alpha
sigma_alpha = alpha * np.sqrt((std_err/slope)**2 + (sigma_intercept/R0)**2)

print(f"R0 = {R0:.3f} ± {sigma_intercept:.3f} Ω")
print(f"α = {alpha:.5f} ± {sigma_alpha:.5f} 1/°C")
print(f"R² = {r_value**2:.5f}")

# Comparación con gas ideal
# Convertir temperatura a Kelvin
T_K = T_real + 273.15

# Presión ideal relativa usando primera medición como referencia
P0 = P_gas[0]
T0 = T_K[0]
P_ideal = P0 * T_K / T0  # Pa

# Gráficos

# 1) Resistencia vs Temperatura
plt.figure(figsize=(6,4))
plt.errorbar(T_real, R_pt100, yerr=dR, xerr=dT_real, fmt='o', label='Datos experimentales')
plt.plot(T_real, intercept + slope*T_real, 'r-', label=f'Ajuste lineal')
plt.xlabel('(Temperatura ± 1) °C')
plt.ylabel('(Resistencia PT100 ± 0.1) Ω')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('resistencia_vs_temperatura.png', dpi=300)
plt.show()

# 2) Altura mercurio vs Temperatura
plt.figure(figsize=(6,4))
plt.errorbar(T_real, h_mercurio, yerr=dh, xerr=dT_real, fmt='o')
plt.xlabel('(Temperatura ± 1) °C')
plt.ylabel('(Altura del mercurio ± 0.05) cm')
plt.grid(True)
plt.tight_layout()
plt.savefig('altura_mercurio_vs_temperatura.png', dpi=300)
plt.show()

# 3) Presión del bulbo vs Temperatura y gas ideal
plt.figure(figsize=(6,4))
plt.errorbar(T_real, P_gas/1000, yerr=rho*g*dh/1000, xerr=dT_real, fmt='o', label='Medida')
plt.plot(T_real, P_ideal/1000, 'r-', label='Gas ideal')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Presión (kPa)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('presion_vs_temperatura.png', dpi=300)
plt.show()


