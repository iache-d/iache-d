import numpy as np
import matplotlib.pyplot as plt

# 1. Rango del eje X (beta * epsilon)
# De -5 a 5 alcanza de sobra para ver las asíntotas
b_eps = np.linspace(-5, 5, 500)

# 2. Energía esperada <E>/eps 
# Usamos senos y cosenos hiperbólicos porque escribir exponenciales a mano da pereza y es propenso a errores
# Metí el 2 multiplicando directo al otro 2 para ahorrar cálculos innecesarios
e_promedio = -4 * np.sinh(b_eps) / (2 * np.cosh(b_eps) + 1)

# 3. pinturamosus
plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})
fig, ax = plt.subplots(figsize=(10, 6))

# 4. Curva principal
ax.plot(b_eps, e_promedio, color='#9467bd', linewidth=3, label=r'$\langle E \rangle / \varepsilon$')

# 5. Guías visuales para no perdernos
# Centro exacto del gráfico (T infinita, el caos total)
ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)

# Asíntotas: qué pasa cuando se congela el universo (T -> 0)
# T -> 0+ (Estado fundamental, todos quietos y aburridos en E=-2)
ax.axhline(y=-2, color='#d62728', linestyle='--', linewidth=2, label=r'$T \to 0^+$ (Estado base)')
# T -> 0- (Inversión de población, modo láser activado en E=+2)
ax.axhline(y=2, color='#1f77b4', linestyle='--', linewidth=2, label=r'$T \to 0^-$ (Energía máx)')

# Pintamos el fondo para distinguir q
ax.axvspan(0, 5, color='#d62728', alpha=0.1, label='T Positiva (Lo normal)')
ax.axvspan(-5, 0, color='#1f77b4', alpha=0.1, label='T Negativa (Inversión térmica)')

# Marcamos el cruce por el origen
ax.plot(0, 0, 'ko', markersize=8)
ax.annotate(r'$T \to \pm\infty$', xy=(0.2, 0.2), fontsize=14)

# 6. Etiquetas 
ax.set_title('Energía Esperada vs Parámetro $\\beta$', fontsize=18, fontweight='bold', pad=15)
ax.set_xlabel(r'Parámetro adimensional $\beta\varepsilon \quad (\propto 1/T)$', fontsize=16)
ax.set_ylabel(r'Energía adimensional $\langle E \rangle / \varepsilon$', fontsize=16)

# Bloqueamos los límites antes de que matplotlib decida hacer auto-zoom donde no debe
ax.set_xlim(-5, 5)
ax.set_ylim(-2.5, 2.5)

ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='best', fontsize=12, framealpha=0.9)

plt.tight_layout()

# Guardar y huir
plt.savefig('energia_esperada_vs_beta.png', dpi=300)
print("Gráfico exportado. Si algo sale mal, culpen a la termodinámica.")
