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

## **Experiencia 3 — Análisis del coeficiente de difusión**

En esta experiencia se estudió el movimiento aleatorio de una partícula utilizando datos experimentales de posición $x(t)$ y $y(t)$.  
A partir de estos datos se calculó el desplazamiento radial $r(t)$, el desplazamiento cuadrático medio $\langle r^2(t)\rangle$ y se obtuvo el coeficiente de difusión mediante un ajuste lineal.

La relación fundamental utilizada fue:

$$
r(t) = \sqrt{(x(t) - x_0)^2 + (y(t) - y_0)^2}
$$

y el desplazamiento cuadrático medio:

$$
\langle r^2(t)\rangle = \frac{1}{N} \sum_{i=1}^{N} r_i^2(t)
$$

El coeficiente de difusión se obtuvo usando:

$$
D = \frac{1}{4} \frac{d}{dt}\langle r^2(t)\rangle
$$

**Script incluido:**

- **[`analisis_coeficiente_difusion.py`](./Experiencias/Experiencia_3/Scripts/analisis_coeficiente_difusion.py)**  
  Procesa los datos, calcula $r(t)$, $r^2(t)$, su promedio, el error estándar, realiza un ajuste lineal y determina el coeficiente de difusión junto con su incertidumbre.  
  Además genera y exporta un gráfico comparando los datos y el ajuste.

---


## **Experiencia 4 — Ajuste exponencial y determinación de viscosidad**

En esta experiencia se analizaron dos aspectos distintos del movimiento:

1. El ajuste exponencial de velocidades para tres esferas de distinto tamaño.
2. La determinación de la viscosidad de un fluido a partir de mediciones de velocidad terminal.


### **Ajuste exponencial de las velocidades**

Se utilizó la función:

$$
v(t) = a e^{bt} + c
$$

para ajustar los datos de tres configuraciones experimentales (esfera pequeña, mediana y grande).  
El primer script:

- Realiza el ajuste de cada conjunto de datos.
- Genera curvas suavizadas.
- Exporta un gráfico comparativo.

**Script:**  
[`ajuste_exponencial_esferas.py`](./Experiencias/Experiencia_4/Scripts/ajuste_exponencial_esferas.py)


### **Determinación de la viscosidad**

A partir de las mediciones de velocidad vertical $v_y(t)$ en múltiples lanzamientos, se calculó el desplazamiento final y la velocidad terminal de cada prueba.

La densidad de la bolita se obtuvo mediante:

$$
\rho_{\text{bolita}} = \frac{m}{\frac{4}{3}\pi r^3}
$$

La viscosidad del fluido se estimó utilizando la ley de Stokes:

$$
\eta = \frac{2}{9} \frac{r^2\left(\rho_{\text{bolita}} - \rho_{\text{medio}}\right) g}{v_f}
$$

El segundo script:

- Lee cinco archivos experimentales.
- Grafica las velocidades $v_y(t)$.
- Calcula las velocidades terminales.
- Obtiene $\eta$ para cada lanzamiento.
- Calcula el promedio y su error estándar.

**Script:**  
[`viscosidad_stokes_lanzamientos.py`](./Experiencias/Experiencia_4/Scripts/viscosidad_stokes_lanzamientos.py)

---

## Experiencia 5 — Equivalente eléctrico del calor

En esta experiencia se estudió la relación entre el trabajo eléctrico entregado al sistema y el calor absorbido por el conjunto agua–calorímetro.  
El objetivo fue determinar el equivalente eléctrico del calor verificando la proporcionalidad entre:

$$
W_e \quad \text{y} \quad Q_{agua}
$$

mediante propagación de errores y un ajuste lineal.

### Parte 1 — Cálculo de $$W_e$$, $$Q_{agua}$$ y sus incertidumbres

Las expresiones utilizadas fueron:

$$
W_e = V I t
$$

$$
Q_{agua} = (m_{agua}\, c_{agua} + m_{cal}\, c_{cal})\, \Delta T
$$

Se aplicó propagación de errores a ambas magnitudes.

**Script incluido:**

- `calculo_trabajo_y_calor_con_errores.py`

### Parte 2 — Ajuste lineal entre trabajo eléctrico y calor absorbido

Se emplearon valores experimentales de $$Q_{agua}$$ y $$W_e$$.  
Luego se realizó un ajuste lineal del tipo:

$$
W_e = a\, Q_{agua} + b
$$

A partir del ajuste se obtuvo:

- La pendiente $$a$$, correspondiente al equivalente eléctrico del calor.  
- El error estándar de la pendiente.  
- El coeficiente de correlación $$R^2$$.  
- El gráfico final `grafico_trabajo_calor_parte2.png`.

**Script incluido:**

- `ajuste_equivalente_electrico_calor.py`

---

