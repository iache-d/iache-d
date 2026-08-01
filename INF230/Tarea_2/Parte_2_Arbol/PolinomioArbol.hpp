#ifndef POLINOMIO_ARBOL_HPP
#define POLINOMIO_ARBOL_HPP

#include <iostream>

/*****
* struct NodoArbol
******
* Nodo del árbol binario de búsqueda que representa un monomio del polinomio.
******
* Input:
* int exp : Exponente del monomio
* int coef : Coeficiente del monomio
******
* Returns:
* Constructor, inicializa el nodo con los valores entregados y punteros izquierdo/derecho en nullptr
*****/
struct NodoArbol {
    int exponente;
    int coeficiente;
    NodoArbol* izquierdo;
    NodoArbol* derecho;

    NodoArbol(int exp, int coef) : exponente(exp), coeficiente(coef), izquierdo(nullptr), derecho(nullptr) {}
};

/*****
* class PolinomioArbol
******
* Clase que representa un polinomio como un árbol binario de búsqueda ordenado por exponentes.
* Provee operaciones para insertar, evaluar (usando el algoritmo de Horner) y obtener coeficientes.
*****/
class PolinomioArbol {
public:
    // Capacidad del arreglo auxiliar usado al evaluar. Los monomios que excedan este
    // limite se ignoran en lugar de escribir fuera del arreglo.
    static const int MAX_MONOMIOS = 100;

private:
    NodoArbol* raiz;

    /*****
    * void insertarRec
    ******
    * Inserta un monomio en el árbol de forma recursiva.
    ******
    * Input:
    * NodoArbol*& nodo : nodo actual del árbol
    * int exponente : exponente del monomio
    * int coeficiente : coeficiente del monomio
    ******
    * Returns:
    * void, no retorna valor
    *****/
    void insertarRec(NodoArbol*& nodo, int exponente, int coeficiente);

    /*****
    * int obtenerCoeficienteRec
    ******
    * Busca recursivamente el coeficiente de un exponente dado.
    ******
    * Input:
    * NodoArbol* nodo : nodo actual
    * int exponente : exponente a buscar
    ******
    * Returns:
    * int, coeficiente correspondiente o 0 si no existe
    *****/
    int obtenerCoeficienteRec(NodoArbol* nodo, int exponente) const;

    /*****
    * void destruirArbol
    ******
    * Libera toda la memoria dinámica del árbol de forma recursiva.
    ******
    * Input:
    * NodoArbol* nodo : nodo actual
    ******
    * Returns:
    * void, no retorna valor
    *****/
    void destruirArbol(NodoArbol* nodo);

    /*****
    * void recolectarEnOrdenInverso
    ******
    * Recolecta todos los nodos del árbol en un arreglo, en orden decreciente de exponente.
    * Esto permite aplicar el algoritmo de Horner en la evaluación.
    ******
    * Input:
    * NodoArbol* nodo : nodo actual
    * NodoArbol* (&arr)[MAX_MONOMIOS] : arreglo de punteros a nodos
    * int& indice : índice actual de inserción en el arreglo
    ******
    * Returns:
    * void, el arreglo queda lleno con nodos en orden descendente
    *****/
    void recolectarEnOrdenInverso(NodoArbol* nodo, NodoArbol* (&arr)[MAX_MONOMIOS], int& indice) const;

public:
    /*****
    * Constructor PolinomioArbol
    ******
    * Inicializa un polinomio vacío representado como un árbol nulo.
    ******
    * Input:
    * Ninguno
    ******
    * Returns:
    * void, constructor
    *****/
    PolinomioArbol();

    /*****
    * Destructor ~PolinomioArbol
    ******
    * Libera toda la memoria dinámica utilizada por el polinomio.
    ******
    * Input:
    * Ninguno
    ******
    * Returns:
    * void, destructor
    *****/
    ~PolinomioArbol();

    /*****
    * void insertarMonomio
    ******
    * Inserta o actualiza un monomio en el árbol. Se mantiene ordenado por exponente.
    ******
    * Input:
    * int exponente : exponente del monomio
    * int coeficiente : coeficiente correspondiente
    ******
    * Returns:
    * void, no retorna valor
    *****/
    void insertarMonomio(int exponente, int coeficiente);

    /*****
    * int obtenerCoeficiente
    ******
    * Retorna el coeficiente correspondiente a un exponente dado.
    ******
    * Input:
    * int exponente : exponente a consultar
    ******
    * Returns:
    * int, coeficiente correspondiente o 0 si no existe
    *****/
    int obtenerCoeficiente(int exponente) const;

    /*****
    * float evaluar
    ******
    * Evalúa el polinomio para un valor de x dado usando el algoritmo de Horner.
    * Los términos son procesados desde el mayor exponente al menor para mayor eficiencia.
    ******
    * Input:
    * float x : valor en el cual se evaluará el polinomio
    ******
    * Returns:
    * float, resultado numérico de la evaluación
    *****/
    float evaluar(float x) const;
};

#endif
