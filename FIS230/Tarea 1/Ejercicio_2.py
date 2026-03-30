import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress 

# 1. Puntos leídos (a ojo) del gráfico
diams = np.array([0.5, 0.7, 1.0, 1.4, 2.0, 3.5]) 
pasante = np.array([0.04, 0.08, 0.10, 0.15, 0.42, 0.98]) 

# 2. Transformación logarítmica (un poco de magia oscura para linealizar Weibull)
x_log = np.log(diams)
y_log = np.log(-np.log(1 - pasante))

# 3. Regresión lineal (Y = mX + b)
# Desempaquetamos lo útil, los '_' son para ignorar cosas que hoy no nos importan (como el p-value)
m, b, r_val, _, _ = linregress(x_log, y_log)

# 4. Rescate de parámetros
beta = m  # Pendiente directa

# Intercepto b = -beta * ln(alfa). Despejando alfa para no sufrir después:
alfa = np.exp(-b / beta)

# Prints al grano
print("Parámetros de Weibull:")
print(f"Beta (forma): {beta:.4f}")
print(f"Alfa (escala): {alfa:.4f} mm")
print(f"R^2: {r_val**2:.4f}\n") # Si esto da muy bajo, toca repensar la vida

# 5. Calculamos el D50 (la mitad de la roca)
d50 = alfa * (np.log(2))**(1/beta)

print(f"D_50 estimado: {d50:.4f} mm\n")

# 6. Gráfico
import matplotlib.pyplot as plt # De nuevo por si corres solo esta celda y se te olvidó el import de arriba

# Datos crudos para plotear
d_obs = np.array([0.15, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 3.5, 5.0])
f_obs = np.array([0.0, 0.0, 0.0, 0.04, 0.08, 0.10, 0.15, 0.42, 0.98, 1.0])

# Rango continuo (500 puntitos son suficientes para engañar al ojo)
x_plot = np.logspace(np.log10(0.1), np.log10(10), 500)

# Curva teórica con la ec. de Weibull
f_weibull = 1 - np.exp(-(x_plot / alfa)**beta)

plt.figure(figsize=(10, 6))

# a. Datos originales
# scatter huecos (facecolors='none') porque se ven más pro
plt.scatter(d_obs, f_obs, s=80, facecolors='none', edgecolors='blue', 
            linewidth=1.5, label='Datos crudos')

# b. Curva teórica Weibull
plt.plot(x_plot, f_weibull, 'r-', linewidth=2, 
            label=f'Ajuste ($\\alpha$={alfa:.2f}, $\\beta$={beta:.2f})')

# c. Marcador del D50
plt.plot(d50, 0.5, 'go', markersize=8, label=f'D50 = {d50:.2f} mm')

# Líneas guías del D50 (matemática fea de matplotlib para que calce bien en escala log)
plt.axhline(0.5, xmin=0, xmax=(np.log10(d50) - np.log10(0.1)) / (np.log10(10) - np.log10(0.1)), 
            color='green', linestyle='--', alpha=0.5)
plt.axvline(d50, ymin=0, ymax=0.5, color='green', linestyle='--', alpha=0.5)

# Setup de ejes
plt.xscale('log') # Sin esto la granulometría no tiene sentido visual
plt.xlim(0.1, 10) # Clavamos los límites a mano para que la escala no haga cosas raras
plt.ylim(-0.05, 1.05)

plt.xlabel('Diámetro $d_i$ [mm]')
plt.ylabel('F($d_i$)')
plt.title('Ajuste Granulométrico Weibull')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3) 

plt.tight_layout() 
plt.savefig('granulometria_d50.png', dpi=300) 
print("Gráfico guardado exitosamente.")
