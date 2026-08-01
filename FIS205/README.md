# FIS205 — Física Computacional

Tareas del curso **FIS205 (Física Computacional)**, resueltas en Jupyter Notebook. Cada
notebook combina el desarrollo analítico, la implementación numérica y la discusión de los
resultados.

> ✅ **Reproducibilidad:** los notebooks no dependen de archivos externos — generan sus propios
> datos y traen las salidas guardadas, por lo que las figuras y tablas se ven directamente en
> GitHub sin ejecutar nada.

**Dependencias:** ver `requirements.txt` en la raíz del repositorio.

---

## 📁 Tarea 1

### Problema 1 — Cadena de espines 1/2: modelo de Ising en campo transversal

[`Tarea_1/Problema1.ipynb`](./Tarea_1/Problema1.ipynb)

Estudio del crecimiento exponencial del espacio de Hilbert y de sus consecuencias sobre la
simulación clásica de sistemas cuánticos de muchos cuerpos.

**Hamiltoniano implementado:**

$$
H = B\sum_{i=1}^{N}\sigma^z_i + J\sum_{i=1}^{N-1}\sigma^x_i\,\sigma^x_{i+1}
$$

Se construye por productos tensoriales sucesivos (`np.kron`) de las matrices de Pauli sobre los
$N$ espines, lo que da una matriz de dimensión $d = 2^N$.

**Contenido:**

- **(a)** Deducción de la dimensión del espacio de Hilbert: $d = 2^N$.
- **(b)** Construcción del Hamiltoniano para $N$ espines arbitrario.
- **(c)** Evolución temporal del estado inicial $|\downarrow\downarrow\cdots\downarrow\rangle$ y
  cálculo de la probabilidad de retorno $|\langle\psi_0|\psi(t)\rangle|^2$ para tres regímenes:
  $B/J \ll 1$, $B/J = 1$ y $B/J \gg 1$. El operador de evolución de un paso
  $U_{\Delta t} = e^{-iH\Delta t}$ se calcula **una sola vez** fuera del bucle, ya que $H$ es
  constante; dentro del bucle solo se aplican productos matriz–vector.
- **(d)** Benchmark del tiempo de diagonalización (`numpy.linalg.eigh`) para $N = 4,\dots,8$,
  promediando 10 corridas por tamaño y descartando el arranque en frío de NumPy.
- **(e)** Ajuste exponencial de los tiempos medidos y extrapolación a $N = 20, 50, 100$.

**Resultado central:** la diagonalización densa escala como
$\mathcal{O}(d^3) = \mathcal{O}(8^N)$. La extrapolación da tiempos de cómputo del orden de
$10^{14}$ años para $N = 50$ — miles de veces la edad del universo — lo que constituye la
motivación histórica de la computación cuántica propuesta por Feynman en 1982.

---

### Problema 2 — Transformada de Fourier discreta: DFT directa vs FFT

[`Tarea_1/Problema2.ipynb`](./Tarea_1/Problema2.ipynb)

Implementación de la DFT desde su definición y comparación de complejidad frente al algoritmo
FFT.

**Señal analizada:** dos armónicos superpuestos, muestreados a $f_s = 1000$ Hz durante 1 s:

$$
x(t) = \sin(2\pi \cdot 50\,t) + 0.5\,\sin(2\pi \cdot 120\,t)
$$

**Contenido:**

- Implementación directa de la DFT por su definición, con doble sumatoria
  $X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i k n/N}$, de complejidad $\mathcal{O}(N^2)$.
- Espectro de amplitud normalizado ($2|X_k|/N$), que recupera las amplitudes físicas
  1.0 y 0.5 en 50 Hz y 120 Hz.
- Verificación numérica contra `numpy.fft.fft`.
- Benchmark para $N = 10^2, 10^3, 10^4, 10^5$ y ajuste log–log de los exponentes de
  complejidad de ambos algoritmos.
- Discusión del impacto de la FFT en física computacional (métodos espectrales para EDPs) y en
  tecnología (telefonía móvil, resonancia magnética, procesamiento de señales en tiempo real).

> **Nota sobre el benchmark:** la DFT directa se compila con `numba` en modo paralelo para que
> los tamaños grandes terminen en un tiempo razonable. Los tiempos absolutos, por tanto, no son
> los de un bucle puro de Python; el **exponente** medido en el ajuste log–log sí refleja la
> complejidad $\mathcal{O}(N^2)$ del algoritmo.

---

### Problema 4 — Dinámica molecular de un gas ideal ($H_2$)

[`Tarea_1/Problema4.ipynb`](./Tarea_1/Problema4.ipynb)

Simulación de $N = 125$ moléculas de hidrógeno confinadas en una caja cúbica, con cálculo de
propiedades termodinámicas a partir del movimiento microscópico.

**Modelo:** gas ideal (sin interacciones entre moléculas), integrado con el método de Euler
explícito y condiciones de frontera reflectantes:

$$
\vec{r}_i(t + \Delta t) = \vec{r}_i(t) + \vec{v}_i(t)\,\Delta t
$$

**Propiedades calculadas:**

| Magnitud | Expresión |
|---|---|
| Temperatura (equipartición) | $T = \dfrac{2}{3}\dfrac{E_k}{N k_B}$ |
| Presión (transferencia de momento) | $P = \dfrac{1}{A}\dfrac{\Delta p}{\Delta t}$, con $\Delta p = 2m\lvert v_\perp\rvert$ por choque |
| Distribución de rapideces | $f(v) = 4\pi v^2\left(\dfrac{m}{2\pi k_B T}\right)^{3/2}e^{-mv^2/2k_BT}$ |

Las velocidades iniciales se sortean de una normal con $\sigma_v = \sqrt{k_B T/m}$, y se verifica
que la distribución de rapideces resultante siga la ley de Maxwell–Boltzmann.

> ⚠️ **Este notebook es interactivo** (`ipywidgets`): los parámetros de temperatura y tamaño de
> la caja se controlan con deslizadores. **GitHub no ejecuta widgets**, por lo que la
> visualización aparece vacía en el navegador. Para verla hay que descargar el notebook y
> ejecutarlo localmente.

---

## 📁 Tarea 2

### Problema 1 — Problema inverso del oscilador amortiguado mediante aprendizaje automático

[`Tarea_2/Problema1.ipynb`](./Tarea_2/Problema1.ipynb)

Recuperación de los parámetros físicos de un sistema a partir de su señal observada: dada
$x(t)$ con ruido, inferir $(\gamma, k)$.

**Sistema directo:**

$$
\ddot{x}(t) + \gamma\,\dot{x}(t) + k\,x(t) = 0,\qquad x(0)=1,\;\dot{x}(0)=0
$$

cuya solución subamortiguada es
$x(t) = e^{-\gamma t/2}\left[\cos(\omega_d t) + \frac{\gamma}{2\omega_d}\sin(\omega_d t)\right]$,
con $\omega_d = \sqrt{k - \gamma^2/4}$.

**Contenido:**

- **(a)** Discusión del problema directo (bien planteado) frente al inverso, y de por qué este
  último no admite una inversión analítica directa.
- **(b)** Generación del conjunto de datos: 3000 señales de 1000 puntos en $t\in[0,10]$,
  integrando la EDO con `scipy.integrate.solve_ivp`, con $\gamma\sim\mathcal{U}(0.05,\,1.0)$,
  $k\sim\mathcal{U}(1.0,\,5.0)$ y ruido gaussiano $\sigma = 0.02$. Se ilustra por separado el
  efecto de $k$ sobre la frecuencia y de $\gamma$ sobre el decaimiento.
- **(c)** Entrenamiento de dos regresores multi-salida: **Random Forest** (200 árboles) y
  **perceptrón multicapa** (capas ocultas de 128 y 64 neuronas). En el MLP se estandarizan
  entradas *y* salidas, para que $k$ —de mayor magnitud— no domine la función de pérdida y la
  red no descuide $\gamma$. Evaluación mediante RMSE por parámetro y gráficos de predicho vs real.
- **(d)** Estudio de la degradación del desempeño frente al ruido, con
  $\sigma \in \{0,\,0.01,\,0.02,\,0.05,\,0.10\}$, comparando error de entrenamiento y de
  validación para detectar sobreajuste.

**Resultado central:** el error crece monótonamente con el ruido, y $\gamma$ resulta más fácil
de recuperar que $k$. El Random Forest supera consistentemente al MLP en este problema.

---

### Problema 2 — Pico de Bragg: transporte de protones en agua

[`Tarea_2/Problema2.ipynb`](./Tarea_2/Problema2.ipynb)

Cálculo del poder de frenado y simulación del depósito de dosis de un haz de protones, con
aplicación directa en protonterapia.

**Poder de frenado (Bethe–Bloch)** para protones en agua, con potencial medio de excitación
$I = 75$ eV y cinemática relativista. El rango CSDA se obtiene integrando numéricamente:

$$
R_\text{CSDA}(E_0) = \int_{E_\text{min}}^{E_0}\frac{dE}{(-dE/dx)(E)}
$$

**Validación contra los valores tabulados de NIST PSTAR (agua líquida):**

| $E_0$ (MeV) | $S$ modelo (MeV cm²/g) | $S$ NIST | error | $R$ modelo (g/cm²) | $R$ NIST | error |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 50 | 12.457 | 12.44 | 0.14% | 2.220 | 2.227 | 0.31% |
| 150 | 5.445 | 5.443 | 0.04% | 15.765 | 15.77 | 0.03% |
| 250 | 3.911 | 3.910 | 0.02% | 37.929 | 37.94 | 0.03% |

**Contenido:**

- **(a)** Origen físico del pico de Bragg: la dependencia $S \propto 1/\beta^2$ hace que el
  protón deposite cada vez más energía a medida que se frena, produciendo un máximo agudo justo
  antes de detenerse.
- **(b)** Implementación de Bethe–Bloch y del rango CSDA, validados contra NIST.
- **(c)** Simulación del transporte de $10^4$ protones de 150 MeV en pasos de 0.1 mm, y
  construcción de la curva de dosis en profundidad $D(z)$. El pico resulta en
  $z \approx 15.79$ cm frente a $R_\text{CSDA} \approx 15.76$ cm, dentro de la resolución del bin.
- **(d)** Incorporación del *straggling* energético mediante la varianza de Bohr
  $\sigma_E^2 = K\,m_ec^2\,\rho\,(Z/A)\,(z^2/\beta^2)\,\Delta x$, y análisis del ensanchamiento
  del pico.

> **Nota de implementación (inciso d).** A alta energía $\sigma_E$ es comparable a
> $\langle\Delta E\rangle$ por paso, de modo que muestrear de una gaussiana literal produce
> valores $\Delta E < 0$, sin sentido físico. Truncar en cero sesgaría el rango, por lo que se
> muestrea de una distribución **gamma** con la misma media y varianza, que converge a la
> gaussiana cuando $\sigma_E \ll \langle\Delta E\rangle$.

**Resultado central:** el straggling **no desplaza** la posición media del pico (rango medio
15.80 cm frente a $R_\text{CSDA} = 15.76$ cm), pero lo **ensancha y reduce** notablemente: la
altura cae de ~150 MeV/cm en el caso CSDA ideal a ~27 MeV/cm.

---

## Contacto

Si encuentras algún error o tienes preguntas sobre alguno de los notebooks, puedes abrir un
*Issue* en este repositorio.
