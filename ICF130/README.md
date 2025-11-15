# ICF130 — Tareas y Proyectos

Este repositorio contiene las tareas y proyectos numéricos desarrollados para el curso **ICF130**.
Cada certamen o tarea incluye los scripts relevantes y una breve descripción del objetivo de cada uno.

---

## 🔹 C1 Numérico: Análisis de Ciclo Termodinámico

Este proyecto corresponde a la parte numérica del Certamen 1. El análisis se presenta como un **Jupyter Notebook** (`.ipynb`) que compara un ciclo termodinámico de 5 etapas para un Gas Ideal (IG) versus un Gas de Van der Waals (VdW).

El notebook principal se encuentra en: [`analisis_ciclo_termo.py`](<./C1Numérico/analisis_ciclo_termo.py>)

### 🧠 Estructura del Notebook

El notebook está dividido en 5 células de ejecución principales que deben correrse en orden:

**1. Célula 1: Configuración y Modelos**
* Importa las bibliotecas necesarias (`numpy`, `matplotlib`, `scipy`).
* Define las constantes globales (R, n) y los datos iniciales del ciclo (T1, P1, P2, T3, P4).
* Define las ecuaciones de estado para el Gas Ideal (`P_ideal`) y Van der Waals (`P_vdw`).
* Carga los datos experimentales sintéticos para el ajuste.

**2. Célula 2: Ajuste de Parámetros VdW**
* Utiliza `scipy.optimize.least_squares` para ajustar los parámetros `a` y `b` de la ecuación de Van der Waals a los datos experimentales.
* Imprime los valores óptimos de `a` y `b` y sus métricas de ajuste (R²).

**3. Célula 3: Cálculo de Estados del Ciclo**
* Resuelve el ciclo de 5 estados (adiabático, isocórico, isotermo, isobárico, isocórico).
* Resuelve los estados analíticamente para el Gas Ideal.
* Utiliza `scipy.optimize.fsolve` para resolver numéricamente el sistema de ecuaciones para el modelo de Van der Waals.
* Imprime y muestra tablas comparativas (usando `pandas`) de (T, P, V) para cada estado.

**4. Célula 4: Análisis Termodinámico (W, Q, η)**
* Define funciones para calcular el Trabajo (W) y el Calor (Q) para cada tipo de proceso (adiabático, isotermo, etc.) para ambos modelos.
* Calcula `W_net`, `Q_net` y la eficiencia térmica ($\eta$) del ciclo completo para IG y VdW.
* Imprime un resumen de los resultados.

**5. Célula 5: Visualización Comparativa**
* Utiliza `matplotlib` para generar los gráficos P-V y T-V.
* Superpone las curvas del ciclo para el Gas Ideal (línea azul) y el Gas de Van der Waals (línea roja punteada) para una comparación visual.

---

### 🛠️ Bibliotecas y Ejecución

El notebook requiere `numpy`, `matplotlib`, `scipy` y `pandas` (para las tablas).

1.  **Instalación (si es necesario):**
    ```bash
    pip install numpy matplotlib scipy pandas jupyter
    ```

2.  **Ejecución:**
    Navega a la carpeta `ICF130` y ejecuta Jupyter:
    ```bash
    jupyter notebook
    ```
    Luego, abre el archivo `C1Numérico/analisis_ciclo_termo.ipynb` desde el navegador y ejecuta las células en orden (Run All).
