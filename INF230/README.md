# INF230 — Tareas y Proyectos

Este repositorio contiene las tareas y proyectos desarrollados para el curso **INF230**.
Cada tarea incluye los scripts relevantes y una breve descripción del objetivo de cada uno.

---

## 🔹 Tarea 1: Gestor de Asistencia

Este programa de consola, desarrollado en C++, calcula el número total de personas (asistentes y empleados) presentes en un evento en una hora específica, basándose en registros de entrada y salida de dos archivos fuente distintos.

El script principal se encuentra en: [`./Tarea 1/gestor_asistencia.cpp`](./Tarea 1/gestor_asistencia.cpp).

### 🚀 Características

* **Consulta por Hora:** El usuario puede ingresar una hora específica en formato `hh:mm` para consultar el estado del evento.
* **Procesamiento de Asistentes:** Lee datos desde un archivo **binario** (`flujo-asistentes.dat`) que registra las variaciones de flujo (cuántas personas entran o salen a la vez).
* **Procesamiento de Empleados:** Lee datos desde un archivo de **texto** (`control-empleados.txt`) que registra el estado individual de cada empleado (ingreso 'I' o salida 'O') basado en su RUT.
* **Reporte Detallado:** Muestra por consola el conteo separado de asistentes, empleados y el total de personas en el evento.

---

### 📂 Archivos Requeridos

Para que el programa funcione, necesita dos archivos en el mismo directorio que el ejecutable (es decir, dentro de `Tarea 1` si compilas allí):

**1. `flujo-asistentes.dat` (Binario)**

Este archivo almacena el flujo de asistentes. Su estructura es:

1.  **Cabecera:** Un solo `int` que indica el número total de registros (N) que contiene el archivo.
2.  **Registros:** N bloques de `VariacionFlujo`, donde cada bloque es un `struct` que contiene:
    * `int hora`: La hora del evento (0-23).
    * `int minuto`: El minuto del evento (0-59).
    * `int cantidad`: La variación neta (positivo si entran, negativo si salen).

**2. `control-empleados.txt` (Texto)**

Este archivo almacena el control de acceso de los empleados. Cada línea tiene el siguiente formato:
`[ESTADO] [RUT] [HORA]`

* **`[ESTADO]`**: Un string, "I" para ingreso (IN) u "O" para salida (OUT).
* **`[RUT]`**: Un string que identifica al empleado.
* **`[HORA]`**: Un string con la hora del evento en formato `hh:mm`.

---

### 🧠 Lógica de Cálculo

* **Asistentes:** Lee todos los registros del archivo binario. Suma las `cantidad` de todos los registros cuya hora sea *menor o igual* a la hora de consulta.
* **Empleados:** Lee el archivo de texto línea por línea. Mantiene un registro del *último estado* conocido de cada RUT. Solo considera los eventos ocurridos en o antes de la hora de consulta. Al final del análisis, cuenta cuántos empleados tienen como último estado 'I' (ingresado).

---

### 🛠️ Compilación y Ejecución

Para compilar y ejecutar, se recomienda estar dentro de la carpeta `Tarea 1`.

1.  **Navegar a la carpeta:**
    ```bash
    cd "Tarea 1"
    ```

2.  **Compilar el programa:**
    ```bash
    g++ gestor_asistencia.cpp -o gestor_asistencia
    ```

3.  **Ejecutar el programa:**
    ```bash
    ./gestor_asistencia
    ```

4.  **Usar el programa:**
    Al ejecutarlo, te pedirá la hora de consulta.

    ```
    Ingrese la hora a consultar (hh:mm): 14:30
    Cantidad de asistentes: 150
    Cantidad de empleados: 12
    Total de personas en el evento: 162
    ```
