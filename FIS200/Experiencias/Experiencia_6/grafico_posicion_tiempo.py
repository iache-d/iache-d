import numpy as np
import matplotlib.pyplot as plt

filename = "XP7FIS200 L3.txt"

with open(filename, "r") as file:
    data = file.readlines()

tiempo = []
posicion = []

for line in data:
    values = line.replace(",", ".").split()

    if len(values) == 2:
        tiempo.append(float(values[0]))
        posicion.append(float(values[1]))

tiempo = np.array(tiempo)
posicion = np.array(posicion)

plt.figure(figsize=(10, 6))
plt.plot(tiempo, posicion, label="Posición vs Tiempo")
plt.xlabel("(Tiempo ± 0.1) s")
plt.ylabel("(Posición ± 0.0001) m")
plt.legend()
plt.grid(True)
plt.savefig("XP7FIS200 L1.png", dpi=300)
plt.show()

# Mostrar la gráfica
plt.grid(True)

# Guardar la gráfica con 300 DPI
plt.savefig('XP7FIS200 L1.png', dpi=300)

# Mostrar la gráfica
plt.show()
