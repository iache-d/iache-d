import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_path_1 = "FIS200XP9 BL1.txt"
file_path_2 = "FIS200XP9 BL2.txt"

data1 = pd.read_csv(
    file_path_1,
    sep="\t",
    names=["t", "theta", "omega"],
    skiprows=1,
    usecols=[1, 2],
    decimal=",",
)

data2 = pd.read_csv(
    file_path_2,
    sep="\t",
    names=["t", "theta", "omega"],
    skiprows=1,
    usecols=[1, 2],
    decimal=",",
)


data1 = data1.dropna()
data1 = data1[~data1.isin([float("inf"), float("-inf")]).any(axis=1)]
data2 = data2.dropna()
data2 = data2[~data2.isin([float("inf"), float("-inf")]).any(axis=1)]

fig, ax = plt.subplots(figsize=(10, 8))

ax.set_xlabel("(Posición Angular ± 0.0001) θ", fontsize=18)
ax.set_ylabel("(Velocidad Angular ± 0.0001) ω", fontsize=18)
ax.grid(True)
ax.set_xlim(30, 160)
ax.set_ylim(-360, 420)

(line1,) = ax.plot([], [], "o-", color="b", label="Masa Superior")
(line2,) = ax.plot([], [], "o-", color="r", label="Masa Inferior")

ax.legend(fontsize=13)


def update(frame):
    line1.set_data(data1["theta"][:frame], data1["omega"][:frame])
    line2.set_data(data2["theta"][:frame], data2["omega"][:frame])
    return line1, line2


# Crear la animación
ani = FuncAnimation(fig, update, frames=len(data1), interval=150, blit=True)

ani.save("grafico_dinamico.gif", writer="pillow")

plt.show()
