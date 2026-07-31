# Imports y parámetros iniciales
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares, fsolve
from scipy.integrate import solve_ivp, quad

# Constantes globales

R = 0.08314   # [L·bar·mol⁻¹·K⁻¹]
n = 1.0       # mol

# Estado inicial
T1 = 300.0    # K
P1 = 6.0      # bar

# Relación de calores para gas ideal (diatómico)
Cv_ig = (5/2) * R
Cp_ig = Cv_ig + R
gamma_ig = Cp_ig / Cv_ig  # ~1.4


# Datos del ciclo
P2 = 12.0   # bar   (final compresión adiabática)
T3 = 480.0  # K     (final calentamiento isocórico)
P4 = 5.0    # bar   (final expansión isotérmica)


# Modelos termodinámicos
def P_ideal(T, V):
    """Ecuación de estado de gas ideal."""
    return n * R * T / V

def P_vdw(T, V, a, b):
    """Ecuación de Van der Waals."""
    return (n * R * T) / (V - n*b) - a * n**2 / V**2


# Datos experimentales sintéticos (para ajuste de a y b)
T_exp = np.array([290, 290, 290, 310, 310, 310, 330, 330, 330, 350, 350, 350])
V_exp = np.array([2.20, 3.00, 4.00, 2.20, 3.00, 4.00, 2.20, 3.00, 4.00, 2.20, 3.00, 4.00])
P_real = np.array([10.8961, 7.9453, 5.9791, 11.6485, 8.5182, 6.4777, 12.3720, 9.1024, 6.9526, 13.0912, 9.6846, 7.4272])  

print("✅ Bloque inicial cargado. Listo para ajuste y simulación del ciclo.")

# Ajuste de parámetros (a, b) de Van der Waals 

def residuals(params, T, V, P_exp):
    a, b = params
    return P_exp - P_vdw(T, V, a, b)

# Estimación inicial razonable
x0 = [1.0, 0.05]

# Ajuste con mínimos cuadrados
result = least_squares(residuals, x0, args=(T_exp, V_exp, P_real))

a_fit, b_fit = result.x
print("Ajuste Van der Waals:")
print(f"a estimado = {a_fit:.4f} L²·bar/mol²")
print(f"b estimado = {b_fit:.4f} L/mol")

# Intervalos de confianza aproximados
J = result.jac
res_var = np.sum(result.fun**2) / (len(P_real) - len(result.x))
cov = np.linalg.inv(J.T @ J) * res_var
param_std = np.sqrt(np.diag(cov))

print("\nIntervalos de confianza 95% aprox:")
print(f"a = {a_fit:.4f} ± {1.96*param_std[0]:.4f}")
print(f"b = {b_fit:.4f} ± {1.96*param_std[1]:.4f}")

# Métricas de ajuste
ss_res = np.sum(result.fun**2)
ss_tot = np.sum((P_real - np.mean(P_real))**2)
r2 = 1 - ss_res/ss_tot

print("\nMétricas de ajuste:")
print(f"RSS = {ss_res:.4f}")
print(f"R² = {r2:.4f}")


from scipy.optimize import fsolve

# Obtener a_fit, b_fit desde result
a_fit, b_fit = result.x
print(f"Usando a_fit = {a_fit:.6f}, b_fit = {b_fit:.6f}")

# --- función auxiliar: buscar V dado T y P para VdW (robusta) ---
def find_V_for_P_vdw(T, P_target, a, b, guess=1.0):
    """Devuelve V tal que P_vdw(T,V,a,b) = P_target. Usa fsolve con varios 'guesses' si es necesario."""
    guesses = [guess, max(guess, 0.5), guess*2, guess*5, 10.0]
    for g in guesses:
        try:
            sol = fsolve(lambda V: P_vdw(T, V, a, b) - P_target, g, xtol=1e-12, maxfev=4000)
            V = float(sol[0])
            # validar solución (V > b*n)
            if V > n*b + 1e-9:
                return V
        except Exception:
            pass
    raise RuntimeError(f"No se encontró V para T={T}, P={P_target} (intentos con guesses {guesses}).")

# --- Estado 1 ---
V1_ig = n * R * T1 / P1                     # [L] gas ideal
V1_vdw = find_V_for_P_vdw(T1, P1, a_fit, b_fit, guess=V1_ig)  # iniciar cerca de V1_ig

# --- Proceso 1 -> 2 : adiabático (compresión) ---



# IG (cerrado, reversible): T2 = T1 * (P2/P1)^((γ-1)/γ)
T2_ig = T1 * (P2 / P1) ** ((gamma_ig - 1) / gamma_ig)
V2_ig = n * R * T2_ig / P2

# VdW: resolver sistema [P(T2,V2)=P2, adiabática VdW]
def eqs_vdw_adiab(vars):
    T2, V2 = vars
    eq1 = P_vdw(T2, V2, a_fit, b_fit) - P2
    # adiabática con Cv constante: Cv ln(T2/T1) + R ln((V2 - n b)/(V1 - n b)) = 0
    eq2 = Cv_ig * np.log(T2 / T1) + R * np.log((V2 - n*b_fit) / (V1_vdw - n*b_fit))
    return [eq1, eq2]


init_guess = [max(T2_ig, 1.0), max(0.6*V1_vdw, n*b_fit + 1e-6)]
sol = fsolve(eqs_vdw_adiab, init_guess, xtol=1e-12, maxfev=8000)
T2_vdw, V2_vdw = float(sol[0]), float(sol[1])

# --- Proceso 2 -> 3 : isocórico (V constante), T -> T3 ---
V3_ig, V3_vdw = V2_ig, V2_vdw
T3_ig = T3_vdw = T3
P3_ig = n * R * T3_ig / V3_ig
P3_vdw = P_vdw(T3_vdw, V3_vdw, a_fit, b_fit)

# --- Proceso 3 -> 4 : isotermo a T3, hasta P4 ---
T4_ig = T4_vdw = T3
V4_ig = n * R * T4_ig / P4
V4_vdw = find_V_for_P_vdw(T4_vdw, P4, a_fit, b_fit, guess=V4_ig)

# --- Proceso 4 -> 5 : isobárico (P=P4) hasta V5 = V1 ---
V5_ig, V5_vdw = V1_ig, V1_vdw  # enunciado dice V5 = V1
T5_ig = P4 * V5_ig / (n * R)
# encontrar T5_vdw tal que P_vdw(T5_vdw, V5_vdw) == P4
T5_vdw = float(fsolve(lambda T: P_vdw(T, V5_vdw, a_fit, b_fit) - P4, T5_ig, xtol=1e-12, maxfev=4000)[0])

# --- Proceso 5 -> 1 : isocórico (V constante), T -> T1 ---
P1_check_ig = n * R * T1 / V5_ig
P1_check_vdw = P_vdw(T1, V5_vdw, a_fit, b_fit)

# --- Reunir resultados ---
states_ig = [
    ("1", T1, P1, V1_ig),
    ("2", T2_ig, P2, V2_ig),
    ("3", T3_ig, P3_ig, V3_ig),
    ("4", T4_ig, P4, V4_ig),
    ("5", T5_ig, P4, V5_ig),
]

states_vdw = [
    ("1", T1, P1, V1_vdw),
    ("2", T2_vdw, P2, V2_vdw),
    ("3", T3_vdw, P3_vdw, V3_vdw),
    ("4", T4_vdw, P4, V4_vdw),
    ("5", T5_vdw, P4, V5_vdw),
]

# --- Imprimir resultados legibles ---
print("\nEstados (Gas Ideal):")
for label, T, P, V in states_ig:
    print(f"{label}: T={T:.4f} K, P={P:.4f} bar, V={V:.6f} L")

print("\nEstados (Van der Waals):")
for label, T, P, V in states_vdw:
    print(f"{label}: T={T:.4f} K, P={P:.4f} bar, V={V:.6f} L")


try:
    import pandas as pd
    df_ig = pd.DataFrame(states_ig, columns=["estado","T[K]","P[bar]","V[L]"])
    df_vdw = pd.DataFrame(states_vdw, columns=["estado","T[K]","P[bar]","V[L]"])
    display(df_ig)
    display(df_vdw)
except Exception:
    pass
# Funciones auxiliares 
def work_ig(T1, V1, T2, V2, process="adiabatic"):
    """Trabajo para gas ideal."""
    if process == "adiabatic":
        # W = ΔU = Cv*(T2-T1) en adiabático reversible
        return -Cv_ig * (T2 - T1)
    elif process == "isothermal":
        return n * R * T1 * np.log(V2/V1)
    elif process == "isobaric":
        # Presión constante ideal (usamos el estado inicial)
        P = n * R * T1 / V1
        return P * (V2 - V1)
    elif process == "isochoric":
        return 0.0
    else:
        raise ValueError("Proceso no reconocido")

def work_vdw(T1, V1, T2, V2, a, b, process="adiabatic"):
    """Trabajo aproximado para Van der Waals integrando P(V)dV con signo correcto.

    """
    # Crear array de V en orden creciente para la integral
    if V2 > V1:
        V_vals = np.linspace(V1, V2, 200)
        sign = 1
    else:
        V_vals = np.linspace(V2, V1, 200)
        sign = 1  # corregir signo si compresión
    
    if process == "adiabatic":
        # Temperatura según adiabática de VdW con Cv constante
        T_vals = T1 * ((V1 - n*b)/(V_vals - n*b))**(R/Cv_ig)
        P_vals = P_vdw(T_vals, V_vals, a, b)
        W = -sign * np.trapezoid(P_vals, V_vals)
    elif process == "isothermal":
        T_vals = T1 * np.ones_like(V_vals)
        P_vals = P_vdw(T_vals, V_vals, a, b)
        W = sign * np.trapezoid(P_vals, V_vals)
    elif process == "isobaric":
        # P constante = P(T,V) evaluado en el promedio de estados
        P_avg = P_vdw((T1+T2)/2, (V1+V2)/2, a, b)
        W = P_avg * (V2 - V1)  # signo ya viene del orden V2-V1

    elif process == "isochoric":
        W = 0.0
    else:
        raise ValueError("Proceso no reconocido")
    
    return W



def heat_ig(T1, T2, V1, V2, process="adiabatic"):
    """Calor para gas ideal"""
    if process == "adiabatic":
        return 0.0
    elif process == "isothermal":
        return n * R * T1 * np.log(V2/V1)
    elif process == "isobaric":
        return Cp_ig * (T2 - T1)
    elif process == "isochoric":
        return Cv_ig * (T2 - T1)
    else:
        raise ValueError("Proceso no reconocido")

def heat_vdw(T1, T2, V1, V2, a, b, process="adiabatic"):
    """Calor aproximado para VdW con Cv constante"""
    if process == "adiabatic":
        return 0.0
    elif process == "isothermal":
        return work_vdw(T1, V1, T2, V2, a, b, process="isothermal")
    elif process == "isobaric":
        return Cp_ig * (T2 - T1)
    elif process == "isochoric":
        return Cv_ig * (T2 - T1)
    else:
        raise ValueError("Proceso no reconocido")


# Lista de procesos del ciclo 
processes = [
    ("1->2","adiabatic"),
    ("2->3","isochoric"),
    ("3->4","isothermal"),
    ("4->5","isobaric"),
    ("5->1","isochoric")
]

#  Inicializar listas para resultados
W_ig_list, Q_ig_list = [], []
W_vdw_list, Q_vdw_list = [], []

#  Estados IG y VdW 
T_states_ig = [T1, T2_ig, T3_ig, T4_ig, T5_ig, T1]
V_states_ig = [V1_ig, V2_ig, V3_ig, V4_ig, V5_ig, V1_ig]

T_states_vdw = [T1, T2_vdw, T3_vdw, T4_vdw, T5_vdw, T1]
V_states_vdw = [V1_vdw, V2_vdw, V3_vdw, V4_vdw, V5_vdw, V1_vdw]

#  Calcular W y Q para cada proceso 
for i, (label, proc_type) in enumerate(processes):
    # Gas Ideal
    W = work_ig(T_states_ig[i], V_states_ig[i], T_states_ig[i+1], V_states_ig[i+1], process=proc_type)
    Q = heat_ig(T_states_ig[i], T_states_ig[i+1], V_states_ig[i], V_states_ig[i+1], process=proc_type)
    W_ig_list.append(W)
    Q_ig_list.append(Q)
    
    # VdW
    W = work_vdw(T_states_vdw[i], V_states_vdw[i], T_states_vdw[i+1], V_states_vdw[i+1], a_fit, b_fit, process=proc_type)
    Q = heat_vdw(T_states_vdw[i], T_states_vdw[i+1], V_states_vdw[i], V_states_vdw[i+1], a_fit, b_fit, process=proc_type)
    W_vdw_list.append(W)
    Q_vdw_list.append(Q)

# Sumar para neto y eficiencia 
Wnet_ig = sum(W_ig_list)
Qnet_ig = sum(Q_ig_list)
eta_ig = Wnet_ig / sum([q for q in Q_ig_list if q>0])  # eficiencia: Wnet / Q_in

Wnet_vdw = sum(W_vdw_list)
Qnet_vdw = sum(Q_vdw_list)
eta_vdw = Wnet_vdw / sum([q for q in Q_vdw_list if q>0])

#  Mostrar resultados 
print("\n--- Gas Ideal ---")
for (label,proc), W,Q in zip(processes,W_ig_list,Q_ig_list):
    print(f"{label} ({proc}): W={W:.4f} bar·L, Q={Q:.4f} bar·L")
print(f"W_net = {Wnet_ig:.4f} bar·L, Q_net = {Qnet_ig:.4f} bar·L, η = {eta_ig:.4f}")

print("\n--- Van der Waals ---")
for (label,proc), W,Q in zip(processes,W_vdw_list,Q_vdw_list):
    print(f"{label} ({proc}): W={W:.4f} bar·L, Q={Q:.4f} bar·L")
print(f"W_net = {Wnet_vdw:.4f} bar·L, Q_net = {Qnet_vdw:.4f} bar·L, η = {eta_vdw:.4f}")

#  Gráficas P-V y T-V
import matplotlib.pyplot as plt

# interpolar
def interp_states(V_start, V_end, T_start, T_end, n_points=100, process="linear"):
    V_vals = np.linspace(V_start, V_end, n_points)
    if process == "linear":
        T_vals = np.linspace(T_start, T_end, n_points)
    elif process == "adiabatic":
        T_vals = T_start * (V_start / V_vals) ** (gamma_ig - 1)  # IG adiabática
    return V_vals, T_vals

#  Preparar curvas para IG---
V_ig_curve = []
P_ig_curve = []
T_ig_curve = []

for i, (label, proc_type) in enumerate(processes):
    V_start, V_end = V_states_ig[i], V_states_ig[i+1]
    T_start, T_end = T_states_ig[i], T_states_ig[i+1]

    if proc_type == "adiabatic":
        V_vals = np.linspace(V_start, V_end, 200)
        T_vals = T_start * (V_start / V_vals) ** (gamma_ig - 1)
        P_vals = n*R*T_vals/V_vals
    elif proc_type == "isothermal":
        V_vals = np.linspace(V_start, V_end, 200)
        P_vals = n*R*T_start / V_vals
        T_vals = np.full_like(V_vals, T_start)
    elif proc_type == "isobaric":
        V_vals = np.linspace(V_start, V_end, 200)
        P_vals = np.full_like(V_vals, P_states_ig := [n*R*T/V for T,V in zip(T_states_ig,V_states_ig)][i])
        T_vals = T_start + (T_end - T_start)*(V_vals - V_start)/(V_end - V_start)
    elif proc_type == "isochoric":
        V_vals = np.full(200, V_start)
        T_vals = np.linspace(T_start, T_end, 200)
        P_vals = n*R*T_vals / V_vals

    V_ig_curve.append(V_vals)
    P_ig_curve.append(P_vals)
    T_ig_curve.append(T_vals)

#  Preparar curvas para VdW 
V_vdw_curve = []
P_vdw_curve = []
T_vdw_curve = []

for i, (label, proc_type) in enumerate(processes):
    V_start, V_end = V_states_vdw[i], V_states_vdw[i+1]
    T_start, T_end = T_states_vdw[i], T_states_vdw[i+1]

    V_vals = np.linspace(V_start, V_end, 200)
    if proc_type == "adiabatic":
        T_vals = T_start * ((V_start - n*b_fit)/(V_vals - n*b_fit)) ** (R/Cv_ig)
    elif proc_type == "isothermal":
        T_vals = np.full_like(V_vals, T_start)
    else:  # isobaric o isochoric
        T_vals = np.linspace(T_start, T_end, 200)
    P_vals = P_vdw(T_vals, V_vals, a_fit, b_fit)

    V_vdw_curve.append(V_vals)
    P_vdw_curve.append(P_vals)
    T_vdw_curve.append(T_vals)

#  Graficar P-V 
plt.figure(figsize=(8,6))
for V_vals, P_vals in zip(V_ig_curve, P_ig_curve):
    plt.plot(V_vals, P_vals, 'b', label='IG' if 'IG' not in plt.gca().get_legend_handles_labels()[1] else "")
for V_vals, P_vals in zip(V_vdw_curve, P_vdw_curve):
    plt.plot(V_vals, P_vals, 'r--', label='VdW' if 'VdW' not in plt.gca().get_legend_handles_labels()[1] else "")
plt.xlabel("V [L]")
plt.ylabel("P [bar]")
plt.title("Ciclo P-V: Gas Ideal vs Van der Waals")
plt.legend()
plt.grid(True)
plt.show()

# Graficar T-V 
plt.figure(figsize=(8,6))
for V_vals, T_vals in zip(V_ig_curve, T_ig_curve):
    plt.plot(V_vals, T_vals, 'b', label='IG' if 'IG' not in plt.gca().get_legend_handles_labels()[1] else "")
for V_vals, T_vals in zip(V_vdw_curve, T_vdw_curve):
    plt.plot(V_vals, T_vals, 'r--', label='VdW' if 'VdW' not in plt.gca().get_legend_handles_labels()[1] else "")
plt.xlabel("V [L]")
plt.ylabel("T [K]")
plt.title("Ciclo T-V: Gas Ideal vs Van der Waals")
plt.legend()
plt.grid(True)
plt.show()


# IG
plt.figure(figsize=(6,5))
for V_vals, P_vals in zip(V_ig_curve, P_ig_curve):
    plt.plot(V_vals, P_vals, 'b')
plt.xlabel("V [L]"); plt.ylabel("P [bar]"); plt.title("Ciclo P-V Gas Ideal"); plt.grid(True)
plt.show()

# VdW
plt.figure(figsize=(6,5))
for V_vals, P_vals in zip(V_vdw_curve, P_vdw_curve):
    plt.plot(V_vals, P_vals, 'r')
plt.xlabel("V [L]"); plt.ylabel("P [bar]"); plt.title("Ciclo P-V Van der Waals"); plt.grid(True)
plt.show()


# Gas Ideal
plt.figure(figsize=(6,5))
for V_vals, T_vals in zip(V_ig_curve, T_ig_curve):
    plt.plot(V_vals, T_vals, 'b')
plt.xlabel("V [L]")
plt.ylabel("T [K]")
plt.title("Ciclo T-V Gas Ideal")
plt.grid(True)
plt.show()

# Van der Waals
plt.figure(figsize=(6,5))
for V_vals, T_vals in zip(V_vdw_curve, T_vdw_curve):
    plt.plot(V_vals, T_vals, 'r')
plt.xlabel("V [L]")
plt.ylabel("T [K]")
plt.title("Ciclo T-V Van der Waals")
plt.grid(True)
plt.show()
