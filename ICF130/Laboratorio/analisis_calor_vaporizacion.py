import numpy as np
import matplotlib.pyplot as plt

# --- Datos experimentales (proporcionados) ---
tiempo_min = np.arange(34)  # 0..33
temperatura = np.array([6.9, 8.5, 11.9, 15, 18.5, 21.9, 25.0, 28.2, 32, 35,
                        39.5, 43.3, 47.2, 50.7, 54.4, 57.7, 60.9, 64.5,
                        67.4, 71.0, 74.2, 77.0, 80.4, 82.9, 85.5, 87.7,
                        91.3, 92.7, 94.0, 95.6, 96.9, 97.4, 97.5, 97.6])
voltaje = np.array([9.29, 9.18, 9.25, 9.23, 9.27, 9.25, 9.24, 9.25, 9.24, 9.28,
                    9.22, 9.21, 9.21, 9.20, 9.20, 9.19, 9.18, 9.18,
                    9.17, 9.14, 9.14, 9.13, 9.13, 9.12, 9.11, 9.10,
                    9.10, 9.14, 9.14, 9.13, 9.13, 9.13, 9.10, 9.10])
I = 5.3  # A constante

# --- Incertidumbres instrumentales ---
delta_T = 0.1  # °C
delta_V = 0.1  # V
delta_I = 0.01  # A

# --- Datos de masa ---
m_total = 200.6 / 1000  # kg (masa total del sistema si hace falta)
# Si mediste masa antes y después del intervalo de ebullición, introduce dm_evap en kg:
# ej: dm_evap = (m_before - m_after)
# La masa de agua evaporada durante la meseta NO quedo registrada en el laboratorio.
# Sin ese dato, L_v no puede calcularse: el script reporta unicamente lo que si se midio
# (el calor entregado durante la meseta) y deja el calculo de L_v pendiente.
# Para completarlo, asignar aqui la masa evaporada en kg y su incertidumbre.
dm_evap = None
dm_evap_unc = None

# --- Convertir tiempo ---
tiempo_s = tiempo_min * 60

# --- Calor acumulado Q(t) (integral) ---
Q_total = np.zeros(len(tiempo_s))
for i in range(1, len(tiempo_s)):
    dt = tiempo_s[i] - tiempo_s[i-1]
    V_avg = 0.5*(voltaje[i] + voltaje[i-1])
    Q_total[i] = Q_total[i-1] + V_avg * I * dt

# --- Detectar meseta de ebullición ---
# estrategia: buscar bloque contiguo cercano a la temperatura máxima (últimos puntos ~97-98 C)
T_max = np.max(temperatura)
# umbral: dentro de (T_max - 1.0) °C (ajustable)
umbral = T_max - 1.0
indices_plateau = np.where(temperatura >= umbral)[0]

# tomar el bloque contiguo final (por si hay puntos aislados)
if len(indices_plateau) == 0:
    raise RuntimeError("No se detectó meseta de ebullición con el umbral actual.")
# elegir el bloque final contiguo
blocks = np.split(indices_plateau, np.where(np.diff(indices_plateau) != 1)[0]+1)
block = blocks[-1]
start_idx, end_idx = block[0], block[-1]

# --- Delta Q durante la meseta (energía suministrada en la meseta) ---
delta_Q_vap = Q_total[end_idx] - Q_total[start_idx]

# --- Obtener/estimar dm_evap ---
L_v_teo = 2.256e6  # J/kg, valor tabulado del agua a 100 °C

print(f"Meseta detectada entre índices {start_idx} y {end_idx} "
      f"(t = {tiempo_min[start_idx]}-{tiempo_min[end_idx]} min).")
print(f"ΔQ durante la meseta = {delta_Q_vap:.1f} J")

if dm_evap is None:
    print()
    print("No se dispone de la masa de agua evaporada, de modo que L_v no puede calcularse.")
    print("Diagnostico: con el ΔQ medido, el valor tabulado L_v = 2.256e6 J/kg")
    print(f"corresponderia a una masa evaporada de {delta_Q_vap / L_v_teo * 1000:.1f} g.")
else:
    # --- Calor latente de vaporización ---
    L_v = delta_Q_vap / dm_evap  # J/kg

    # --- Propagación de errores ---
    # incertidumbre en Q: sumar contribuciones de cada intervalo dentro del bloque
    dQ2 = 0.0
    for i in range(start_idx+1, end_idx+1):
        dt = tiempo_s[i] - tiempo_s[i-1]
        # sensibilidad parcial: dQ/dV = I*dt ; dQ/dI = V_avg*dt
        dQ2 += (delta_V * I * dt)**2 + (delta_I * 0.5*(voltaje[i]+voltaje[i-1]) * dt)**2
    dQ = np.sqrt(dQ2)

    # incertidumbre total en L_v:
    # dL = L_v * sqrt( (dQ/delta_Q)^2 + (dm_unc/dm)^2 )
    dm = dm_evap
    dm_unc = dm_evap_unc if dm_evap_unc is not None else 0.0
    dL_v = abs(L_v) * np.sqrt( (dQ / delta_Q_vap)**2 + (dm_unc / dm)**2 )

    # imprimir resultados
    print(f"Δm_evap = {dm_evap:.4f} kg  (incertidumbre {dm_unc:.4f} kg)")
    print(f"Calor latente de vaporización estimado: L_v = {L_v:.1f} J/kg ± {dL_v:.1f} J/kg")

    # comparación con el valor tabulado
    err_rel = abs(L_v_teo - L_v) / L_v_teo * 100
    print(f"Valor tabulado: {L_v_teo:.1f} J/kg   ->   error relativo: {err_rel:.2f} %")

# --- Gráfica T(Q) y marca de la meseta ---
plt.figure(figsize=(7,4.5))
plt.errorbar(Q_total, temperatura, yerr=delta_T, fmt='o', markersize=4, label='Datos')
# marcar inicio y fin meseta
plt.axvline(Q_total[start_idx], color='C1', linestyle='--', label='Inicio meseta')
plt.axvline(Q_total[end_idx], color='C2', linestyle='--', label='Fin meseta')
plt.xlabel('Calor acumulado Q (J)')
plt.ylabel('Temperatura (°C)')
plt.title('Curva T(Q) - calentamiento y meseta de ebullición')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('curva_TQ_vaporizacion.png', dpi=300)
plt.show()

