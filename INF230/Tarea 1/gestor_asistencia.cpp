#include <iostream> // Biblioteca estándar para entrada y salida.
#include <fstream>  // Biblioteca para manejo de archivos.
#include <sstream>  // Biblioteca para manejo de flujos de texto.
#include <string>   // Biblioteca para manejar cadenas de texto.

using namespace std; // Evita escribir 'std::' antes de funciones de la biblioteca estándar.

typedef struct // Definimos una estructura para almacenar datos de variación de flujo.
{
    int hora;     // Hora del evento (0-23).
    int minuto;   // Minuto del evento (0-59).
    int cantidad; // Variación en la cantidad de asistentes (positivo si entran, negativo si salen).
} VariacionFlujo; // Nombre de la estructura.

// Función para leer el archivo binario y obtener un arreglo dinámico con los datos de variación de flujo.
VariacionFlujo *arregloAsistentes(string archivo, int *cantidad)
{
    ifstream file(archivo, ios::binary); // Abrimos el archivo en modo binario.
    if (!file)                           // Verificamos si el archivo se abrió correctamente.
    {
        cerr << "Error al abrir el archivo de asistentes." << endl; // Mensaje de error si el archivo no se puede abrir.
        *cantidad = 0;                                              // Asignamos 0 a cantidad si hay error.
        return nullptr;                                             // Retornamos un puntero nulo.
    }

    file.read(reinterpret_cast<char *>(cantidad), sizeof(int)); // Leemos la cantidad de registros del archivo.
    VariacionFlujo *registros = new VariacionFlujo[*cantidad];  // Reservamos memoria para almacenar los registros.

    file.read(reinterpret_cast<char *>(registros), (*cantidad) * sizeof(VariacionFlujo)); // Leemos los datos en memoria.
    file.close();                                                                         // Cerramos el archivo.
    return registros;                                                                     // Devolvemos el puntero al arreglo dinámico de registros.
}

// Función que calcula la cantidad total de asistentes hasta una hora determinada.
int cantidadAsistentes(string archivo, string hora)
{
    int total = 0, cantidad;                                       // Inicializamos total de asistentes y cantidad de registros.
    int horaConsulta, minutoConsulta;                              // Variables para almacenar la hora a consultar.
    sscanf(hora.c_str(), "%d:%d", &horaConsulta, &minutoConsulta); // Convertimos el string 'hora' en dos enteros.

    VariacionFlujo *registros = arregloAsistentes(archivo, &cantidad); // Obtenemos los registros desde el archivo binario.
    if (!registros)                                                    // Si no se pudo leer el archivo, retornamos 0.
        return 0;

    for (int i = 0; i < cantidad; i++) // Recorremos los registros.
    {
        if (registros[i].hora < horaConsulta || (registros[i].hora == horaConsulta && registros[i].minuto <= minutoConsulta))
        {
            total += registros[i].cantidad; // Sumamos las variaciones hasta la hora indicada.
        }
    }

    delete[] registros; // Liberamos memoria dinámica.
    return total;       // Devolvemos el total de asistentes.
}

// Función para contar la cantidad de empleados presentes hasta una hora dada.
void cantidadEmpleados(string archivo, string hora, int *cantidad)
{
    ifstream file(archivo); // Abrimos el archivo de empleados en modo texto.
    if (!file)              // Verificamos si se abrió correctamente.
    {
        cerr << "Error al abrir el archivo de empleados." << endl; // Mensaje de error.
        *cantidad = 0;
        return;
    }

    string empleados[1000]; // Arreglo estático para almacenar RUTs de empleados (máx. 1000).
    char estado[1000];      // Arreglo para almacenar su estado ('I' para ingresado, 'O' para salido).
    int numEmpleados = 0;   // Contador de empleados registrados.

    string linea, tipoEvento, rut, horaEvento; // Variables auxiliares.
    int horaConsulta, minutoConsulta, horaArchivo, minutoArchivo;
    sscanf(hora.c_str(), "%d:%d", &horaConsulta, &minutoConsulta); // Convertimos la hora a enteros.

    while (getline(file, linea)) // Leemos línea por línea el archivo.
    {
        istringstream iss(linea);
        iss >> tipoEvento >> rut >> horaEvento;                            // Extraemos tipo de evento, RUT y hora del evento.
        sscanf(horaEvento.c_str(), "%d:%d", &horaArchivo, &minutoArchivo); // Convertimos la hora del archivo a enteros.

        if (horaArchivo < horaConsulta || (horaArchivo == horaConsulta && minutoArchivo <= minutoConsulta)) // Si el evento ocurrió antes o en la hora de consulta.
        {
            bool encontrado = false;               // Bandera para saber si el RUT ya está registrado.
            for (int i = 0; i < numEmpleados; i++) // Buscamos el RUT en el arreglo.
            {
                if (empleados[i] == rut) // Si el RUT ya existe en el arreglo.
                {
                    estado[i] = tipoEvento[0]; // Actualizamos su estado ('I' o 'O').
                    encontrado = true;
                    break;
                }
            }
            if (!encontrado && numEmpleados < 1000) // Si no está registrado y hay espacio disponible.
            {
                empleados[numEmpleados] = rut;        // Almacenamos el RUT.
                estado[numEmpleados] = tipoEvento[0]; // Registramos el estado.
                numEmpleados++;                       // Incrementamos el contador.
            }
        }
    }

    *cantidad = 0;                         // Inicializamos el contador de empleados presentes.
    for (int i = 0; i < numEmpleados; i++) // Recorremos la lista de empleados.
    {
        if (estado[i] == 'I') // Si el estado es 'I' (ingresado), contamos al empleado.
        {
            (*cantidad)++;
        }
    }

    file.close(); // Cerramos el archivo.
}

// Función que devuelve un puntero a un arreglo con la cantidad de asistentes y empleados.
int *cantidadPersonas(string hora)
{
    static int resultado[2];                                         // Arreglo estático para almacenar los resultados.
    resultado[0] = cantidadAsistentes("flujo-asistentes.dat", hora); // Calculamos asistentes hasta la hora dada.
    cantidadEmpleados("control-empleados.txt", hora, &resultado[1]); // Calculamos empleados hasta la hora dada.
    return resultado;                                                // Retornamos el puntero al arreglo de resultados.
}

// Función principal del programa.
int main()
{
    string horaConsulta;                             // Variable para almacenar la hora ingresada por el usuario.
    cout << "Ingrese la hora a consultar (hh:mm): "; // Solicitamos la hora al usuario.
    cin >> horaConsulta;                             // Leemos la hora ingresada.

    int *resultado = cantidadPersonas(horaConsulta);                                     // Llamamos a la función que obtiene los datos.
    cout << "Cantidad de asistentes: " << resultado[0] << endl;                          // Mostramos el número de asistentes.
    cout << "Cantidad de empleados: " << resultado[1] << endl;                           // Mostramos el número de empleados.
    cout << "Total de personas en el evento: " << (resultado[0] + resultado[1]) << endl; // Mostramos el total.

    return 0; // Terminamos la ejecución del programa.
}
