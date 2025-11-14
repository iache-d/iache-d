import numpy as np
import matplotlib.pyplot as plt

# Datos del primer caso (sin roce)
v0 = 0.1537  # Velocidad inicial en m/s
g = 9.81  # Aceleración debido a la gravedad en m/s^2
theta = 1.87  # Ángulo en grados
theta_rad = np.radians(theta)  # Convertir a radianes
a = g * np.sin(theta_rad)  # Aceleración en m/s^2

# Rango de tiempo
t = np.linspace(0, 5, 100)  # De 0 a 5 segundos, 100 puntos

# Calcular velocidad en función del tiempo para el primer caso
v1 = v0 + a * t

# Datos del segundo caso (con roce)
vf2 = 1.5233  # Velocidad final en m/s
gamma2 = 0.11  # Coeficiente de roce en s^-1

# Calcular velocidad en función del tiempo con roce para el segundo caso
v2 = vf2 + (v0 - vf2) * np.exp(-gamma2 * t)

# Datos del tercer caso (con roce)
vf3 = 0.900160  # Velocidad final en m/s
gamma3 = 0.23  # Coeficiente de roce en s^-1

# Calcular velocidad en función del tiempo con roce para el tercer caso
v3 = vf3 + (v0 - vf3) * np.exp(-gamma3 * t)

# Crear gráfico
plt.figure(figsize=(10, 6))
plt.plot(t, v1, label="Caso 1", color="blue")
plt.plot(t, v2, label="Caso 2", color="orange")
plt.plot(t, v3, label="Caso 3", color="green")
plt.xlabel("(Tiempo ± 0,02) s")
plt.ylabel("Velocidad ± 0,001 m/s")
plt.grid()
plt.legend()
plt.savefig("grafico_velocidades_promedio.png", dpi=300)
plt.show()
