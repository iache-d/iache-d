# Importa la librería NumPy para realizar cálculos numéricos eficientes y manejar arreglos (arrays).
import numpy as np
# Importa el módulo pyplot de Matplotlib, que se utiliza para crear visualizaciones y gráficos.
import matplotlib.pyplot as plt
# Importa el módulo stats de SciPy, que contiene una amplia gama de distribuciones y funciones estadísticas.
import scipy.stats as stats

# 1. Transcribimos las frecuencias de la tabla
# Crea un arreglo unidimensional de NumPy que almacena la cantidad absoluta de sismos para cada intervalo de tiempo.
freqs = np.array([
    1369, 570, 500, 400, 300, 210, 180, 160, 140, 120,
    110, 100, 105, 95, 90, 85, 80, 82, 75, 70,
    68, 65, 60, 58, 60, 55, 52, 50, 48, 45,
    42, 40, 38, 37, 36, 35, 34, 32, 31, 30,
    29, 28, 27, 26, 25, 24, 23, 22, 20, 18
])

# Creamos las marcas de clase (el punto medio de cada intervalo: 0.5, 1.5, ..., 49.5)
# Genera un arreglo secuencial que empieza en 0.5, termina antes de 50.0, dando saltos de 1.0.
midpoints = np.arange(0.5, 50.0, 1.0)

# Suma todos los elementos del arreglo freqs para obtener el tamaño total de la muestra empírica (N).
N = np.sum(freqs)

# 2. Calculamos los estadísticos de la muestra
# Calcula la media muestral ponderada: suma del producto de las frecuencias por sus puntos medios, dividida por el total (N).
mean_t = np.sum(midpoints * freqs) / N

# Calcula la varianza muestral ponderada usando la corrección de Bessel (N-1) para obtener un estimador insesgado.
var_t = np.sum(freqs * (midpoints - mean_t)**2) / (N - 1)

# Imprime en la consola el número total de observaciones (N).
print(f"Total de sismos medidos (N): {N}")
# Imprime el valor de la media calculada, formateando la salida a 4 decimales.
print(f"Promedio de tiempo (mu): {mean_t:.4f} hrs")
# Imprime el valor de la varianza calculada, formateando la salida a 4 decimales.
print(f"Varianza (sigma^2): {var_t:.4f} hrs^2\n")

# 3. Estimación de Parámetros (Método de los Momentos)

# Estima el parámetro de tasa (lambda o escala inversa) de la distribución Gamma dividiendo la media entre la varianza.
lambda_gamma = mean_t / var_t
# Estima el parámetro de forma (alfa) de la distribución Gamma elevando la media al cuadrado y dividiendo entre la varianza.
alpha_gamma = (mean_t**2) / var_t



# Estima el parámetro de tasa (lambda) de la distribución Exponencial, que equivale al inverso matemático de la media.
lambda_exp = 1.0 / mean_t

# Imprime un separador de texto para la sección de los parámetros calculados.
print("--- Parámetros Encontrados ---")
# Imprime los parámetros 'alfa' y 'lambda' obtenidos para ajustar el modelo Gamma.
print(f"Distribución Gamma: alfa = {alpha_gamma:.4f}, lambda = {lambda_gamma:.4f}")
# Imprime el parámetro 'lambda' obtenido para ajustar el modelo Exponencial.
print(f"Distrib. Exponencial: lambda = {lambda_exp:.4f}\n")



# Calcula la probabilidad acumulada desde 0 hasta 5 horas para la distribución Gamma. Nota: SciPy usa 'scale' como 1/lambda.
prob_gamma = stats.gamma.cdf(5, a=alpha_gamma, scale=1/lambda_gamma)
# Calcula la probabilidad acumulada desde 0 hasta 5 horas para la distribución Exponencial.
prob_exp = stats.expon.cdf(5, scale=1/lambda_exp)

# Imprime un separador para la sección de resultados de probabilidad.
print("--- Probabilidad de t < 5 hrs ---")
# Muestra la probabilidad según el modelo Gamma, multiplicada por 100 para formato de porcentaje con 2 decimales.
print(f"Según modelo Gamma: {prob_gamma*100:.2f}%")
# Muestra la probabilidad según el modelo Exponencial en formato de porcentaje.
print(f"Según modelo Exponencial: {prob_exp*100:.2f}%")


# 5. Parámetro de bondad de ajuste (Suma de Errores Cuadrados - SSE)

# Crea un arreglo que define los bordes exactos de cada intervalo de tiempo (de 0 a 50 inclusive).
bins = np.arange(0, 51, 1)


# Obtiene un arreglo con las probabilidades de que un valor caiga en cada "cubeta" (bin) restando las áreas acumuladas del modelo Gamma.
prob_intervalos_gamma = np.diff(stats.gamma.cdf(bins, a=alpha_gamma, scale=1/lambda_gamma))
# Hace lo mismo que la línea anterior, pero utilizando la función de distribución acumulada del modelo Exponencial.
prob_intervalos_exp = np.diff(stats.expon.cdf(bins, scale=1/lambda_exp))


# Calcula cuántos sismos teóricos caerían en cada intervalo multiplicando el total (N) por la probabilidad Gamma del intervalo.
freq_esperada_gamma = N * prob_intervalos_gamma
# Calcula la misma frecuencia teórica, pero asumiendo el modelo Exponencial.
freq_esperada_exp = N * prob_intervalos_exp

# Suma de errores cuadrados (SSE): sum( (Observado - Esperado)^2 )
# Calcula el Error Cuadrático para Gamma: resta la frecuencia teórica de la observada, eleva al cuadrado y suma todos los resultados.
sse_gamma = np.sum((freqs - freq_esperada_gamma)**2)
# Calcula el Error Cuadrático para Exponencial siguiendo la misma lógica matemática.
sse_exp = np.sum((freqs - freq_esperada_exp)**2)

# Imprime un separador indicando el inicio del análisis de error.
print("\n--- Análisis de Error (Bondad de Ajuste) ---")
# Imprime en pantalla el valor total del Error Cuadrático de la distribución Gamma.
print(f"Error Cuadrático (SSE) Gamma: {sse_gamma:.2f}")
# Imprime en pantalla el valor total del Error Cuadrático de la distribución Exponencial.
print(f"Error Cuadrático (SSE) Exponencial: {sse_exp:.2f}")

# Estructura condicional: Compara matemáticamente cuál de los dos errores es más pequeño.
if sse_gamma < sse_exp:
    # Si el error Gamma es menor, se concluye e imprime que Gamma es el mejor ajuste.
    print("Conclusión: La distribución Gamma ajusta mejor los datos.")
else:
    # De lo contrario, se concluye e imprime que el modelo Exponencial es superior.
    print("Conclusión: La distribución Exponencial ajusta mejor los datos.")

# 6. Generación del Gráfico Profesional con Matplotlib

# Normalizamos las frecuencias para convertirlas en densidad de probabilidad empírica.
# Densidad = (frecuencia_absoluta / total) / ancho_del_intervalo
# Como el ancho de tus intervalos es 1 (0-1, 1-2, etc.), solo dividimos por N.
# Divide el arreglo de frecuencias absolutas entre el total N, transformando los conteos en proporciones (probabilidades).
densidades_empiricas = freqs / N

# Generamos puntos suaves para dibujar las curvas teóricas (de 0 a 50 horas, 500 puntos)
# Genera 500 puntos distribuidos uniformemente entre 0 y 50 para trazar una línea continua y sin cortes.
x_curva = np.linspace(0, 50, 500)

# Calculamos las funciones de densidad de probabilidad teóricas (PDF)
# Evalúa la Función de Densidad de Probabilidad (PDF) del modelo Gamma en cada uno de los 500 puntos generados.
pdf_gamma_teorica = stats.gamma.pdf(x_curva, a=alpha_gamma, scale=1/lambda_gamma)
# Evalúa la Función de Densidad de Probabilidad (PDF) del modelo Exponencial en los mismos 500 puntos.
pdf_exp_teorica = stats.expon.pdf(x_curva, scale=1/lambda_exp)


# Aumentamos el tamaño de fuente global para mayor claridad
# Modifica los parámetros por defecto del gráfico, definiendo una fuente tamaño 14 sin remates (sans-serif).
plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})

# Creamos la figura y los ejes con un tamaño cómodo y adecuad
# Inicializa el lienzo del gráfico (fig) y la zona de trazado (ax), dándole un tamaño de 12 por 8 pulgadas.
fig, ax = plt.subplots(figsize=(12, 8))


# a) Graficamos el histograma empírico (los datos reales de microsismicidad)
# Usamos un color gris neutro y transparencia para no sobrecargar
# 'align=center' usa las marcas de clase (midpoints) en el centro de las barras.
# Dibuja un gráfico de barras usando las marcas de clase y las densidades. Le da un color gris translúcido y bordes negros.
ax.bar(midpoints, densidades_empiricas, width=1.0, align='center',
        alpha=0.5, color='#7f8c8d', edgecolor='black', 
        label='Datos Empíricos (Observados)')

# b)Graficamos la Curva Gamma (Modelo Ganador)

# Superpone la curva de probabilidad teórica Gamma en rojo continuo con un grosor destacable
ax.plot(x_curva, pdf_gamma_teorica, 
        color='#d62728', linestyle='-', linewidth=3.0,
        label=f'Ajuste Gamma (Ganador)\n($\\alpha={alpha_gamma:.3f}$, $\\lambda={lambda_gamma:.3f}$)')

# c) Graficamos la Curva Exponencial
# Color azul contrastante y línea segmentada (dashed) para distinguir si se imprime en B/N.
# Superpone la curva Exponencial en azul punteado, lo cual ayuda a diferenciarla visualmente de la Gamma.
ax.plot(x_curva, pdf_exp_teorica, 
        color='#1f77b4', linestyle='--', linewidth=2.5,
        label=f'Ajuste Exponencial\n($\\lambda={lambda_exp:.3f}$)')


# Título descriptivo
# Añade el título principal del gráfico, asignándole tamaño 20, formato negrita y un espacio de 20 puntos respecto al borde.
ax.set_title('Modelado de Probabilidad para Intervalos de Tiempo entre Microsismos', 
                fontsize=20, fontweight='bold', pad=20)

# Etiquetas de ejes claras con unidades 
# Nombra el eje X detallando la variable medida (Tiempo) y la unidad específica (horas).
ax.set_xlabel('Tiempo entre sismos ($\\Delta t$ en horas)', fontsize=16, labelpad=15)
# Nombra el eje Y indicando que lo graficado es la densidad de probabilidad.
ax.set_ylabel('Densidad de Probabilidad', fontsize=16, labelpad=15)

# Agregamos una cuadrícula ligera para facilitar la lectura de valores
# Activa las líneas de fondo (cuadrícula), haciéndolas punteadas, grises y un poco transparentes para que no estorbe,
ax.grid(True, linestyle='--', alpha=0.4, color='lightgray')

# Configuramos la leyenda para que sea clara y no tape los datos importantes

# Despliega el recuadro que explica qué es cada color/línea, situándolo arriba a la derecha.
ax.legend(fontsize=14, loc='upper right', frameon=True, shadow=False)

# Ajuste automático del diseño para que no se corten etiquetas
# Instruye a Matplotlib para que auto-acomode los márgenes y asegure que ningún texto o etiqueta quede cortada en la imagen final.
plt.tight_layout()


# Guardamos la imagen en formato PNG a 300 DPI 

# Renderiza el gráfico y lo exporta como un archivo PNG con calidad de impresión (300 DPI) eliminando el espacio en blanco sobrante.
plt.savefig('grafico_microsismicidad.png', dpi=300, bbox_inches='tight')


# Imprime un mensaje final confirmando al usuario que la rutina de creación y guardado de imagen terminó correctamente.
print("\n--- Gráfico generado y guardado como 'grafico_microsismicidad.png' ---")
