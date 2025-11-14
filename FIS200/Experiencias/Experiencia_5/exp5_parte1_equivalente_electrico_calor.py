import numpy as np


V = (3.997 + 3.963 + 3.956) / 3
I = 2.5
t_total = 26

t_total_s = t_total * 60

m_calorimetro = 31.96
m_agua = 156.8 - m_calorimetro
c_agua = 4.186
c_calorimetro = 0.897

# Temperaturas inicial y final
T_i = 25.5
T_f = 46.5
delta_T = T_f - T_i


Q_agua = (m_agua * c_agua + m_calorimetro * c_calorimetro) * delta_T
W_e = V * I * t_total_s


delta_V = 0.05  # Error en V en V
delta_I = 0.01  # Error en I en A
delta_t = 1  # Error en tiempo en s

# Calculo del error de W_e
error_W_e = W_e * np.sqrt(
    (delta_V / V) ** 2 + (delta_I / I) ** 2 + (delta_t / t_total_s) ** 2
)

# Errores de masa y calor específico
delta_m_agua = 0.1  # Error en la masa del agua en g
delta_m_calorimetro = 0.01  # Error en la masa del calorímetro en g
delta_c_agua = 0.01  # Error en el calor específico del agua en J/g°C
delta_c_calorimetro = 0.01  # Error en el calor específico del calorímetro en J/g°C
delta_T_temp = 0.5  # Error en el cambio de temperatura en °C

# Calculo del error de Q_agua
error_Q_agua = Q_agua * np.sqrt(
    (delta_m_agua / m_agua) ** 2
    + (delta_c_agua / c_agua) ** 2
    + (delta_m_calorimetro / m_calorimetro) ** 2
    + (delta_c_calorimetro / c_calorimetro) ** 2
    + (delta_T_temp / delta_T) ** 2
)

# Impresión de resultados, solo el error es lo importante
print(f"Trabajo eléctrico W_e: {W_e:.2f} J ± {error_W_e:.2f} J")
print(f"Calor absorbido Q_agua: {Q_agua:.2f} J ± {error_Q_agua:.2f} J")
