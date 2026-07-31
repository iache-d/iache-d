"""Distancias teóricas de alcance (15°, 30°, 45°) comparadas con las medidas.

K y su incertidumbre se obtienen de `parametros_resorte.py`, no se copian a mano.
"""

import numpy as np

from parametros_resorte import GRAVEDAD, constante_elastica, velocidad_inicial

K, _, sigma_K = constante_elastica()

# Ángulos de lanzamiento
angulos = np.array([15, 30, 45])
angulos_rad = np.radians(angulos)

v0 = velocidad_inicial(K)

# Alcance en tiro parabólico: d = v0² sin(2θ) / g
distancias_teoricas = (v0**2 * np.sin(2 * angulos_rad)) / GRAVEDAD

# Propagación del error: d ∝ K, luego σ_d / d = σ_K / K
errores_teoricos = np.abs(distancias_teoricas) * (sigma_K / K)

# Datos experimentales
distancias_experimentales = np.array([0.596, 0.645, 0.648])
errores_experimentales = np.array([0.006, 0.007, 0.006])

for angulo, d_teorico, d_error_teorico, d_exp, error_exp in zip(
    angulos,
    distancias_teoricas,
    errores_teoricos,
    distancias_experimentales,
    errores_experimentales,
):
    print(f"Ángulo: {angulo} grados")
    print(f"Distancia Teórica: {d_teorico:.3f} ± {d_error_teorico:.3f} m")
    print(f"Distancia Experimental: {d_exp:.3f} ± {error_exp:.3f} m")
    print()
