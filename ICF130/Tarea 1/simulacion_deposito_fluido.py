import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


g = 9.81  # m/s^2

# Depósito
D_T = 4.0  # m
R_T = D_T / 2
A_T = np.pi * R_T**2  # m^2

# Tubería B
D_B = 0.27  # m
R_B = D_B / 2
A_B = np.pi * R_B**2  # m^2

# Tubería C
Q_C = 0.0008  # m^3/s

# Tubería D (Asumiendo D_D = D_A = 38 cm)
D_D = 0.30  # m
R_D = D_D / 2
A_D = np.pi * R_D**2  # m^2

# Límite para h por la fórmula de Q_A
h_limite = 2 ** (1 / 4)


# Esta es la función que gobierna el sistema, f(t, h) = dh/dt
def modelo(t, h):

    h = h[0]

    # OJO: Aplicamos la restricción física de la fórmula
    if h >= h_limite:
        Q_A = 0.0
    else:
        Q_A = 0.5 * np.sqrt(2 - h**4)

    v_B = 3 * np.cos(np.pi * t) + 2
    Q_B = A_B * v_B

    # Asegurarse de que h no sea negativo para la raíz cuadrada
    h_seguro = max(0, h)
    v_D = np.sqrt(2 * g * h_seguro)
    Q_D = A_D * v_D

    Q_in = Q_A + Q_B + Q_C

    Q_out = Q_D

    dh_dt = (Q_in - Q_out) / A_T

    return [dh_dt]


# Debe ser menor que h_limite (1.19 m)
h0 = [0.5]  # Asumimos que el tanque empieza con 0.5 m de agua

# Rango de tiempo para la simulación (en segundos)
t_final = 100  # Simular por 100 segundos
t_span = (0, t_final)

# Puntos de tiempo para evaluar la solución
t_eval = np.linspace(t_span[0], t_span[1], 500)

# Llamar al solucionador
print("Iniciando la simulación numérica...")
sol = solve_ivp(
    modelo, t_span, h0, t_eval=t_eval, method="RK45"  # Método estándar (Runge-Kutta)
)
print("Simulación completada.")


if sol.success:
    plt.figure(figsize=(10, 6))
    plt.plot(sol.t, sol.y[0], label="h(t) - Altura del fluido")
    plt.axhline(
        y=h_limite,
        color="r",
        linestyle="--",
        label=f"Límite de $Q_A$ (h={h_limite:.2f} m)",
    )
    plt.title("Variación de la Altura del Fluido en el Depósito")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Altura h (m)")
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("La simulación falló.")
    print(sol.message)
