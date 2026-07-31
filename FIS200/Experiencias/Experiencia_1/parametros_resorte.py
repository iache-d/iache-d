"""Mediciones y cálculos base de la Experiencia 1 (sistema de lanzamiento por resorte).

Centraliza los datos experimentales y el cálculo de la constante elástica K con su
incertidumbre, de modo que el resto de los scripts los importen en lugar de copiar
valores numéricos a mano. Así, si una medición cambia, todos los resultados que
dependen de ella se actualizan solos.
"""

import numpy as np

# --- Mediciones directas ---
ALTURA = 0.265  # m
MASA = 0.0602  # kg
COMPRESION_RESORTE = 0.029  # m
GRAVEDAD = 9.81  # m/s²

DISTANCIAS_CM = np.array([50.4, 50.9, 50.5, 50.5, 50.6])  # cm
DISTANCIAS_M = DISTANCIAS_CM / 100  # m

# --- Incertidumbres instrumentales ---
SIGMA_M = 0.00001  # kg (0.01 g)
SIGMA_G = 0.0981  # m/s² (1% de 9.81)
SIGMA_H = 0.0005  # m (0.5 mm)
SIGMA_C = 0.0005  # m (0.5 mm)


def constante_elastica():
    """Constante elástica del resorte a partir de la conservación de energía.

    Devuelve (K_promedio, desviacion_estandar_muestral, error_de_propagacion) en N/m.
    """
    k_values = (MASA * GRAVEDAD * DISTANCIAS_M**2) / (
        2 * ALTURA * COMPRESION_RESORTE**2
    )

    k_mean = np.mean(k_values)
    k_std = np.std(k_values, ddof=1)

    sigma_k = k_mean * np.sqrt(
        (SIGMA_M / MASA) ** 2
        + (SIGMA_G / GRAVEDAD) ** 2
        + (SIGMA_H / ALTURA) ** 2
        + (2 * SIGMA_C / COMPRESION_RESORTE) ** 2
    )

    return k_mean, k_std, sigma_k


def estadistica_distancias():
    """Promedio y desviación estándar muestral de las distancias medidas, en metros."""
    return np.mean(DISTANCIAS_M), np.std(DISTANCIAS_M, ddof=1)


def velocidad_inicial(k):
    """Velocidad de salida del proyectil, desde la energía almacenada en el resorte."""
    return np.sqrt((2 * k * COMPRESION_RESORTE**2) / MASA)
