# FIS200 — Códigos y Cálculos

Este repositorio contiene los códigos desarrollados para el curso **FIS200**, organizados por experiencias.  
Cada experiencia incluye los scripts relevantes y una breve descripción del objetivo de cada uno.

---

## 🔹 Experiencias

### **Experiencia 1 — Determinación de la constante elástica, análisis de distancias y comparación teórico–experimental**

En esta experiencia se trabajó con un sistema de lanzamiento usando un resorte comprimido.  
Los objetivos principales fueron:

- Calcular la constante elástica \(K\) a partir de mediciones experimentales.  
- Analizar trayectorias de proyectiles a distintos ángulos.  
- Ajustar curvas promedio y compararlas con tendencias teóricas.  
- Calcular promedios, desviaciones estándar y realizar propagación de errores.  
- Comparar distancias medidas con predicciones físicas.

**Scripts incluidos (haz clic para abrirlos):**

- [`calculo_k_y_error.py`](./Experiencias/Experiencia_1/calculo_k_y_error.py)  
  Cálculo de \(K\), su desviación estándar y propagación de errores.

- [`trayectoria_0_grados.py`](./Experiencias/Experiencia_1/trayectoria_0_grados.py)  
  Lectura de datos experimentales de 0°, normalización de coordenadas, graficación de trayectorias y tendencia promedio.

- [`trayectoria_30_grados.py`](./Experiencias/Experiencia_1/trayectoria_30_grados.py)  
  Procesamiento de datos a 30°, ajuste cuadrático promedio y comparación con la curva teórica.

- [`promedio_y_desviacion.py`](./Experiencias/Experiencia_1/promedio_y_desviacion.py)  
  Cálculo de promedios y desviaciones estándar para distancias medidas.

- [`distancias_teoricas_vs_experimentales.py`](./Experiencias/Experiencia_1/distancias_teoricas_vs_experimentales.py)  
  Cálculo de distancias teóricas para ángulos de 15°, 30° y 45°, incluyendo propagación de errores y comparación con valores experimentales.

---

---

## **Experiencia 2 — Dinámica del movimiento con y sin roce**

En esta experiencia se analizó la evolución temporal de la velocidad de un bloque deslizándose por un riel inclinado bajo tres condiciones distintas: sin roce, con roce débil y con roce más intenso.  

Se implementó un único script que calcula las expresiones de velocidad para cada modelo y genera un gráfico comparativo exportado como `grafico_velocidades_promedio.png`.

**Script incluido:**

- **[`analisis_velocidad_con_y_sin_roce.py`](./Experiencias/Experiencia_2/Scripts/analisis_velocidad_con_y_sin_roce.py)**  
  Contiene el cálculo de:  
- Velocidad sin roce usando:

$$
v(t) = v_0 + a t
$$

- Velocidad con roce lineal usando:

$$
v(t) = v_f + (v_0 - v_f)e^{-\gamma t}
$$

Además genera un gráfico comparativo entre los tres casos.



---

