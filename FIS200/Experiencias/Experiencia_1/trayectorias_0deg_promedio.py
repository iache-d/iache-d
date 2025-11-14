import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Lista de archivos de datos para el ángulo
archivos = [
    "0_grados_lanzamiento1.txt",
    "0_grados_lanzamiento2.txt",
    "0_grados_lanzamiento3.txt",
    "0_grados_lanzamiento4.txt",
    "0_grados_lanzamiento5.txt",
]

plt.figure(figsize=(10, 8))

# Listas para almacenar todas las trayectorias
todas_líneas_x = []
todas_líneas_y = []

for i, archivo in enumerate(archivos, start=1):
    try:
        # Leer datos con coma como separador decimal
        datos = pd.read_csv(archivo, sep="\s+", engine="python", decimal=",")

        # Verificar datos cargados
        print(f"Primeras filas del archivo {archivo}:")
        print(datos.head())

        # Convertir columnas a números
        datos = datos.apply(pd.to_numeric, errors="coerce")

        # Verificar datos convertidos
        print(f"Datos después de conversión a numérico para {archivo}:")
        print(datos.head())

        # Extraer columnas
        x = datos["x"].values
        y = datos["y"].values

        # Filtrar valores válidos
        valid_mask = ~np.isnan(x) & ~np.isnan(y)
        x = x[valid_mask]
        y = y[valid_mask]

        # Verificar datos válidos
        print(f"Datos válidos para {archivo}:")
        print(f"x: {x}")
        print(f"y: {y}")

        x -= x[0]
        y -= y[0]

        # Graficar trayectoria
        plt.plot(x, y, marker="o", linestyle="-", label=f"Lanzamiento {i}")

        # Almacenar trayectorias para calcular la tendencia promedio
        if len(x) > 0:
            todas_líneas_x.append(x)
            todas_líneas_y.append(y)

    except Exception as e:
        print(f"Se produjo un error al procesar el archivo {archivo}: {e}")

# Asegurarse de que todas las trayectorias se procesaron correctamente
if len(todas_líneas_x) == 0:
    print("No se cargaron trayectorias válidas. Revisa los datos de entrada.")
else:
    # Convertir listas a arrays numpy para procesar
    todas_líneas_x = np.array(
        [
            np.interp(np.linspace(0, 1, num=100), np.linspace(0, 1, num=len(x)), x)
            for x in todas_líneas_x
        ]
    )
    todas_líneas_y = np.array(
        [
            np.interp(np.linspace(0, 1, num=100), np.linspace(0, 1, num=len(y)), y)
            for y in todas_líneas_y
        ]
    )

    # Promediar las trayectorias
    x_promedio = np.mean(todas_líneas_x, axis=0)
    y_promedio = np.mean(todas_líneas_y, axis=0)

    # Graficar la línea de tendencia promedio
    plt.plot(
        x_promedio,
        y_promedio,
        linestyle="--",
        color="r",
        label="Tendencia Promedio",
        linewidth=2,
    )

# Configurar límites de los ejes con margen
margen = 0.005
plt.xlim(
    min(np.concatenate(todas_líneas_x)) - margen,
    max(np.concatenate(todas_líneas_x)) + margen,
)
plt.ylim(
    min(np.concatenate(todas_líneas_y)) - margen,
    max(np.concatenate(todas_líneas_y)) + margen,
)


plt.xlabel("Posición en X ± 0.005 m")
plt.ylabel("Posición en Y ± 0.005 m")
plt.grid(True)
plt.legend()
plt.gca().invert_yaxis()


plt.savefig("grafico_0.png", format="png", dpi=300)


plt.show()
