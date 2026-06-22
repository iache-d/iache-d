import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


t_datos = np.array([0.24, 0.28, 0.32, 0.36, 0.40, 0.42, 0.45, 0.50, 0.56, 0.64, 0.74, 0.86, 1.00, 1.20])
senal_datos = np.array([14.6, 42.4, 66.5, 90.9, 97.1, 100.0, 95.3, 88.8, 72.2, 59.1, 37.9, 26.3, 15.5, 8.7])


def modelo_TOF(t, C, b):
    return C * (t**-4) * np.exp(-b / t**2)


parametros_optimos, covarianza = curve_fit(modelo_TOF, t_datos, senal_datos, p0=[20, 0.35])
C_opt, b_opt = parametros_optimos


print("=== RESULTADOS DEL AJUSTE ===")
print(f"Parámetro óptimo C: {C_opt:.4f}")
print(f"Parámetro óptimo b: {b_opt:.4f}")
print("=============================")


t_continuo = np.linspace(0.2, 1.3, 200)
senal_ajustada = modelo_TOF(t_continuo, C_opt, b_opt)

# Configuración del gráfico
plt.figure(figsize=(9, 6))


plt.plot(t_datos, senal_datos, 'ko', label='Datos experimentales (TOF)')
plt.plot(t_continuo, senal_ajustada, 'r-', linewidth=2, 
         label=f'Ajuste modelo: $I(t) = {C_opt:.2f} t^{{-4}} \exp(-{b_opt:.3f}/t^2)$')

# Detalles estéticos
plt.title('Espectro de Tiempo de Vuelo (TOF) para Átomos de Xe', fontsize=14)
plt.xlabel('Tiempo de vuelo $t$ (ms)', fontsize=12)
plt.ylabel('Señal Normalizada', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)

# Mostrar el gráfico final
plt.show()
