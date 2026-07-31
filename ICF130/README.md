# ICF130 — Tareas y Proyectos

Este repositorio contiene las tareas y proyectos numéricos desarrollados para el curso **ICF130**.
Cada certamen o tarea incluye los scripts relevantes y una breve descripción del objetivo de cada uno.

---

## 🔹 Tareas

### Tarea 1: Simulación de Dinámica de Fluidos

Este script modela la dinámica de la altura (`h`) de un fluido en un depósito cilíndrico. El sistema está sujeto a múltiples flujos de entrada y salida, algunos constantes, otros variables con el tiempo y otros dependientes de la altura del fluido.

El script principal se encuentra en: [`simulacion_deposito_fluido.py`](./Tarea_1/simulacion_deposito_fluido.py)

**Lógica del Script:**
1.  **Modelo Físico:** Define una Ecuación Diferencial Ordinaria (EDO) basada en la ley de continuidad para el depósito: $dh/dt = (Q_{\text{in}} - Q_{\text{out}}) / A_{\text{tanque}}$.
2.  **Flujos Complejos:** Los caudales (flujos) son no lineales:
    * $Q_A$ depende de $\sqrt{2 - h^4}$.
    * $Q_B$ varía con el tiempo, $\propto \cos(\pi t)$.
    * $Q_D$ (salida) sigue la ley de Torricelli, $\propto \sqrt{h}$.
3.  **Solución Numérica:** Utiliza `scipy.integrate.solve_ivp` con un método Runge-Kutta (RK45) para resolver la EDO y encontrar la función $h(t)$ para un estado inicial $h_0 = 0.5$ m.
4.  **Visualización:** Genera un gráfico de $h(t)$ vs. Tiempo, mostrando la evolución de la altura del fluido.



---

## 🔹 C1 Numérico: Análisis de Ciclo Termodinámico

Este proyecto corresponde a la parte numérica del Certamen 1. El script de Python analiza un ciclo termodinámico de 5 etapas para un mol de un gas diatómico, comparando el comportamiento de un **Gas Ideal (IG)** con un **Gas de Van der Waals (VdW)**.

El script principal se encuentra en: [`analisis_ciclo_termo.py`](./C1_Numerico/analisis_ciclo_termo.py)

### 🧠 Lógica del Script

El análisis se realiza en cuatro etapas principales:

**1. Ajuste de Parámetros VdW**
* Utiliza `scipy.optimize.least_squares` para ajustar los parámetros `a` y `b` de la ecuación de Van der Waals a un conjunto de datos experimentales sintéticos (P, V, T).
* Calcula los intervalos de confianza y la métrica de ajuste R² para validar el modelo.

**2. Cálculo de Estados del Ciclo**
* Define un ciclo de 5 estados (1→2 adiabático, 2→3 isocórico, 3→4 isotermo, 4→5 isobárico, 5→1 isocórico).
* Resuelve analíticamente los estados para el Gas Ideal.
* Utiliza `scipy.optimize.fsolve` para resolver el sistema de ecuaciones no lineales (termodinámicas y de estado VdW) y encontrar las coordenadas (T, P, V) en cada estado para el modelo de Van der Waals.

**3. Análisis Termodinámico (W, Q, η)**
* Calcula el Trabajo (W) y el Calor (Q) para cada una de las 5 etapas del ciclo, tanto para IG como para VdW.
* Para VdW, el trabajo en procesos no isocóricos se calcula integrando numéricamente $P(T, V) dV$ usando `np.trapezoid`.
* Suma los valores para obtener el Trabajo Neto (`W_net`) y el Calor Neto (`Q_net`).
* Calcula la eficiencia térmica ($\eta = W_{net} / Q_{in}$) del ciclo para ambos modelos.

**4. Visualización Comparativa**
* Utiliza `matplotlib` para generar gráficos P-V y T-V.
* Superpone las curvas del ciclo para el Gas Ideal y el Gas de Van der Waals, permitiendo una comparación visual directa de las desviaciones del comportamiento ideal.

---

### 🛠️ Bibliotecas y Ejecución

El script requiere `numpy`, `matplotlib` y `scipy`.

1.  **Instalación (si es necesario):**
    ```bash
    pip install numpy matplotlib scipy
    ```

2.  **Ejecución:**
    Simplemente ejecuta el script en una terminal desde la carpeta `C1_Numerico`:
    ```bash
    python analisis_ciclo_termo.py
    ```

3.  **Resultados:**
    El script imprimirá en la consola:
    * Los parámetros `a` y `b` de VdW ajustados.
    * Tablas con los valores de (T, P, V) para cada estado (IG y VdW).
    * Tablas con los valores de W y Q para cada proceso (IG y VdW).
    * Los valores netos y la eficiencia (η) de ambos modelos.
    * Mostrará las ventanas de `matplotlib` con los gráficos P-V y T-V.
  
    
---

## 🔹 Laboratorios

Scripts de análisis para los laboratorios del curso.

### Laboratorio 1: Termómetro de Gas y Ley de Gas Ideal

Este script analiza los datos de un experimento de termómetro de gas a volumen constante, comparando su comportamiento con la ley de gas ideal.

El script principal se encuentra en: [`analisis_termometro_gas.py`](./Laboratorio/analisis_termometro_gas.py)

**Lógica del Script:**
1.  **Calibración PT100:** Realiza un ajuste lineal (`scipy.stats.linregress`) a los datos de (T, R) para calibrar el sensor PT100 y obtener su $R_0$ y $\alpha$.
2.  **Cálculo de Presión:** Convierte las mediciones de altura de la columna de mercurio (`h_mercurio`) a Presión (Pa), usando la densidad del mercurio y la presión atmosférica.
3.  **Comparación (Ley de Gay-Lussac):** Calcula la presión teórica (`P_ideal`) que el gas debería tener en cada temperatura si siguiera la ley de gas ideal ($P \propto T$).
4.  **Visualización:** Genera 3 gráficos comparativos, incluyendo `R vs T` (calibración) y `P_medida vs P_ideal` (verificación de la ley).

### Laboratorio 2: Calores Latentes de Fusión y Vaporización

Estos scripts analizan los datos de un calorímetro eléctrico para determinar los calores latentes de fusión y vaporización del agua.

**Parte 1: Calor Latente de Fusión ($L_f$)**
* **Script:** [`analisis_calor_fusion.py`](./Laboratorio/analisis_calor_fusion.py)
* **Lógica:** Determina $L_f$ midiendo la energía eléctrica ($Q = V \cdot I \cdot t$) suministrada durante la meseta de fusión (0°C) para una masa de hielo conocida ($L_f = Q / m_{\text{hielo}}$).

**Parte 2: Calor Latente de Vaporización ($L_v$)**
* **Script:** [`analisis_calor_vaporizacion.py`](./Laboratorio/analisis_calor_vaporizacion.py)
* **Lógica:** Determina $L_v$ midiendo la energía suministrada durante la meseta de ebullición ($\Delta Q$) y dividiéndola por la masa de agua evaporada ($\Delta m_{\text{evap}}$) durante ese tiempo ($L_v = \Delta Q / \Delta m_{\text{evap}}$).
---
