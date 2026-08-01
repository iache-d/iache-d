#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "PolinomioLista.hpp"

/*****
* int main
******
* Función principal que maneja lectura de entrada, procesamiento y escritura de salida
******
* Input:
* Ninguno (archivos externos son usados)
******
* Returns:
* int, 0 si termina correctamente
*****/
int main()
{
    std::ifstream archivoEntrada("inputPolynomial.txt");
    std::ofstream archivoSalida("outputPolynomial.txt");

    if (!archivoEntrada.is_open() || !archivoSalida.is_open())
    {
        std::cerr << "Error al abrir los archivos." << std::endl;
        return 1;
    }

    int N;
    archivoEntrada >> N;

    // Arreglo dinámico de polinomios
    Polinomio* polinomios = new Polinomio[N];

    for (int i = 0; i < N; ++i)
    {
        int M;
        archivoEntrada >> M;
        for (int j = 0; j < M; ++j)
        {
            int exponente, coeficiente;
            archivoEntrada >> exponente >> coeficiente;
            polinomios[i].insertarMonomio(exponente, coeficiente);
        }
    }

    std::string linea;
    std::getline(archivoEntrada, linea); // limpiar salto de línea

    while (std::getline(archivoEntrada, linea))
    {
        std::stringstream ss(linea);
        std::string comando;
        ss >> comando;

        if (comando == "COEFICIENTE")
        {
            int i, j;
            ss >> i >> j;
            archivoSalida << polinomios[i].obtenerCoeficiente(j) << std::endl;
        }
        else if (comando == "EVALUAR")
        {
            int i;
            float x;
            ss >> i >> x;
            archivoSalida << polinomios[i].evaluar(x) << std::endl;
        }
    }

    // Liberar memoria
    delete[] polinomios;

    archivoEntrada.close();
    archivoSalida.close();
    return 0;
}
