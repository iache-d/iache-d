#include <iostream>
#include <fstream>
#include "PolinomioArbol.hpp"

using namespace std;

/*****
* main
******
* Función principal que maneja la lectura de polinomios desde un archivo,
* ejecuta operaciones sobre ellos (obtener coeficiente y evaluación),
* y escribe los resultados en un archivo de salida.
******
* Input:
* Ninguno directo desde el usuario. Lee desde "inputPolynomial.txt" y escribe en "outputPolynomial.txt".
******
* Returns:
* int, 0 si la ejecución fue exitosa
*****/
int main() {
    ifstream entrada("inputPolynomial.txt");   // Archivo de entrada con datos de los polinomios y comandos
    ofstream salida("outputPolynomial.txt");   // Archivo de salida para los resultados

    int N;  // Cantidad de polinomios a procesar
    entrada >> N;

    // Se crea un arreglo dinámico de polinomios
    PolinomioArbol* polinomios = new PolinomioArbol[N];

    // Lectura de cada polinomio
    for (int i = 0; i < N; ++i) {
        int M;  // Cantidad de monomios en el polinomio i
        entrada >> M;
        for (int j = 0; j < M; ++j) {
            int exponente, coeficiente;
            entrada >> exponente >> coeficiente;
            polinomios[i].insertarMonomio(exponente, coeficiente);  // Inserta el monomio en el árbol correspondiente
        }
    }

    // Procesamiento de comandos: "COEFICIENTE i j" o "EVALUAR i x"
    string comando;
    while (entrada >> comando) {
        if (comando == "COEFICIENTE") {
            int i, j;  // i: índice del polinomio, j: exponente a consultar
            entrada >> i >> j;
            salida << polinomios[i].obtenerCoeficiente(j) << endl;  // Resultado al archivo
        } else if (comando == "EVALUAR") {
            int i;       // i: índice del polinomio
            float x;     // x: valor en el que se evaluará el polinomio
            entrada >> i >> x;
            salida << polinomios[i].evaluar(x) << endl;  // Resultado de la evaluación al archivo
        }
    }

    // Liberación de memoria dinámica
    delete[] polinomios;

    // Cierre de archivos
    entrada.close();
    salida.close();

    return 0;
}
