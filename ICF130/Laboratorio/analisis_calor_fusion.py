import numpy as np
import matplotlib.pyplot as plt

# --- Datos experimentales ---
tiempo_min = np.array([0, 1, 2, 3, 4, 5, 6, 7,8,9,10,11])  # minutos

temperatura = np.array([1.1, 1.1, 1.1, 1.1, 1.2, 1.2, 1.3, 1.3,1.4,1.5,1.6,1.7])  # °C

voltaje = np.array([5.7, 5.7, 5.7, 5.7, 5.6, 5.6, 5.6, 5.6, 5.6,5.6,5.5,5.5])  # V

I = 3.5 

# Incertidumbres
delta_T = 0.1  # °C
delta_V = 0.1  # V
delta_I = 0.01  # A

# Masa de hielo agregado
m_hielo = 50.4 / 1000  # kg

# --- Convertimos tiempo a segundos ---
tiempo_s = tiempo_min * 60

# --- Fase considerada para la fusión ---
# Toda la serie registrada permanece entre 1.1 y 1.7 C, de modo que no se distingue una
# meseta de fusión separada de la fase de calentamiento posterior: se usan los 12 puntos.
# Esto sobreestima la energía atribuida al cambio de fase y explica que el L_f resultante
# quede por debajo del valor tabulado de 334 kJ/kg.
indices_fusion = np.arange(len(temperatura))

# --- Calor acumulado Q(t) solo durante la meseta ---
delta_Q_fusion = 0
for i in range(1, len(indices_fusion)):
    idx_prev = indices_fusion[i-1]
    idx_curr = indices_fusion[i]
    dt = tiempo_s[idx_curr] - tiempo_s[idx_prev]
    V_avg = (voltaje[idx_curr] + voltaje[idx_prev]) / 2
    delta_Q_fusion += V_avg * I * dt

# --- Calor latente de fusión ---
L_f = delta_Q_fusion / m_hielo  # J/kg

# --- Propagación de errores ---
dQ = np.sqrt(sum( ((delta_V * I * (tiempo_s[indices_fusion[i]] - tiempo_s[indices_fusion[i-1]]))**2 +
                   (delta_I * ((voltaje[indices_fusion[i]] + voltaje[indices_fusion[i-1]])/2) *
                    (tiempo_s[indices_fusion[i]] - tiempo_s[indices_fusion[i-1]]))**2 )
                for i in range(1, len(indices_fusion))) )
dm = 0.1 / 1000  # error en masa
dL_f = L_f * np.sqrt((dQ/delta_Q_fusion)**2 + (dm/m_hielo)**2)

L_f_teo = 334e3  # J/kg, valor tabulado para el agua
print(f"Calor latente de fusión estimado: L_f = {L_f:.1f} J/kg ± {dL_f:.1f} J/kg")
print(f"Valor tabulado: {L_f_teo:.1f} J/kg   ->   error relativo: "
      f"{abs(L_f_teo - L_f)/L_f_teo*100:.1f} %")

# --- Gráfico T(Q) ---
Q_total = np.zeros(len(tiempo_s))
for i in range(1, len(tiempo_s)):
    dt = tiempo_s[i] - tiempo_s[i-1]
    Q_total[i] = Q_total[i-1] + (voltaje[i] + voltaje[i-1])/2 * I * dt

plt.errorbar(Q_total, temperatura, xerr=0, yerr=delta_T, fmt='o', capsize=5, label='Datos experimentales')
plt.xlabel('Calor acumulado Q (J)')
plt.ylabel('Temperatura (°C)')
plt.title('Curva T(Q) durante la fusión del hielo')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('curva_TQ_fusion.png', dpi=300)
plt.show()
