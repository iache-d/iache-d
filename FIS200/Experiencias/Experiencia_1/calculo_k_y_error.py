"""Constante elástica K del resorte, con desviación estándar y propagación de errores.

Las mediciones y el cálculo viven en `parametros_resorte.py`.
"""

from parametros_resorte import constante_elastica

K_mean, K_std, sigma_K = constante_elastica()

print(f"Promedio de K: {K_mean:.2f} N/m")
print(f"Desviación estándar de K: {K_std:.2f} N/m")
print(f"Error de propagación de K: {sigma_K:.2f} N/m")
