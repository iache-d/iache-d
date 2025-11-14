import numpy as np


def calcular_b_y_error(B, B_delta, m, m_delta):
    # Convertir m a kilogramos
    m_kg = m / 1000
    m_delta_kg = m_delta / 1000

    b = (1 / B) * (2 * m_kg)
    b_delta = b * np.sqrt((B_delta / B) ** 2 + (m_delta_kg / m_kg) ** 2)

    return b, b_delta, m_kg, m_delta_kg


B = 165.889
B_delta = 0.001
m = 40.10
m_delta = 0.01

b, b_delta, m_kg, m_delta_kg = calcular_b_y_error(B, B_delta, m, m_delta)

print(f"El valor calculado de b es: {b:.9f} ± {b_delta:.9f}")
