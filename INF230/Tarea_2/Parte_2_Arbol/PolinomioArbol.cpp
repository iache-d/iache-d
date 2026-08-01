#include "PolinomioArbol.hpp"

/*****
* Constructor PolinomioArbol
******
* Inicializa el árbol del polinomio como vacío (puntero nulo).
******
* Input:
* Ninguno
******
* Returns:
* void, constructor
*****/
PolinomioArbol::PolinomioArbol() {
    raiz = nullptr;
}

/*****
* Destructor ~PolinomioArbol
******
* Libera toda la memoria utilizada por el árbol recursivamente.
******
* Input:
* Ninguno
******
* Returns:
* void, destructor
*****/
PolinomioArbol::~PolinomioArbol() {
    destruirArbol(raiz);
}

/*****
* void destruirArbol
******
* Función auxiliar recursiva que libera memoria de todos los nodos del árbol.
******
* Input:
* NodoArbol* nodo : nodo actual a liberar
******
* Returns:
* void, no retorna valor
*****/
void PolinomioArbol::destruirArbol(NodoArbol* nodo) {
    if (nodo) {
        destruirArbol(nodo->izquierdo);
        destruirArbol(nodo->derecho);
        delete nodo;
    }
}

/*****
* void insertarMonomio
******
* Inserta un nuevo monomio en el árbol, o actualiza su coeficiente si el exponente ya existe.
******
* Input:
* int exponente : exponente del monomio
* int coeficiente : coeficiente del monomio
******
* Returns:
* void, no retorna valor
*****/
void PolinomioArbol::insertarMonomio(int exponente, int coeficiente) {
    insertarRec(raiz, exponente, coeficiente);
}

/*****
* void insertarRec
******
* Inserta un monomio en el árbol de manera recursiva, manteniendo el orden por exponente.
******
* Input:
* NodoArbol*& nodo : referencia al nodo actual
* int exponente : exponente del monomio
* int coeficiente : coeficiente del monomio
******
* Returns:
* void, no retorna valor
*****/
void PolinomioArbol::insertarRec(NodoArbol*& nodo, int exponente, int coeficiente) {
    if (!nodo) {
        nodo = new NodoArbol(exponente, coeficiente);
    } else if (exponente < nodo->exponente) {
        insertarRec(nodo->izquierdo, exponente, coeficiente);
    } else if (exponente > nodo->exponente) {
        insertarRec(nodo->derecho, exponente, coeficiente);
    } else {
        nodo->coeficiente = coeficiente;
    }
}

/*****
* int obtenerCoeficiente
******
* Retorna el coeficiente de un monomio con un exponente dado.
******
* Input:
* int exponente : exponente a buscar
******
* Returns:
* int, coeficiente correspondiente o 0 si no se encuentra
*****/
int PolinomioArbol::obtenerCoeficiente(int exponente) const {
    return obtenerCoeficienteRec(raiz, exponente);
}

/*****
* int obtenerCoeficienteRec
******
* Función recursiva que busca un nodo con el exponente dado y retorna su coeficiente.
******
* Input:
* NodoArbol* nodo : nodo actual
* int exponente : exponente a buscar
******
* Returns:
* int, coeficiente del nodo o 0 si no se encuentra
*****/
int PolinomioArbol::obtenerCoeficienteRec(NodoArbol* nodo, int exponente) const {
    if (!nodo) return 0;
    if (exponente < nodo->exponente) {
        return obtenerCoeficienteRec(nodo->izquierdo, exponente);
    } else if (exponente > nodo->exponente) {
        return obtenerCoeficienteRec(nodo->derecho, exponente);
    } else {
        return nodo->coeficiente;
    }
}

/*****
* float evaluar
******
* Evalúa el polinomio para un valor dado de x usando una técnica similar a Horner.
******
* Input:
* float x : valor en el cual se evaluará el polinomio
******
* Returns:
* float, resultado de la evaluación
*****/
float PolinomioArbol::evaluar(float x) const {
    NodoArbol* nodos[MAX_MONOMIOS]; // arreglo auxiliar para almacenar nodos
    int indice = 0;
    recolectarEnOrdenInverso(raiz, nodos, indice);

    if (indice == 0) return 0.0f;

    // El arbol guarda unicamente los monomios presentes, de modo que el polinomio es
    // disperso: entre dos nodos consecutivos puede haber grados ausentes. Por eso el
    // esquema de Horner debe avanzar segun la diferencia de exponentes y no de uno en
    // uno, y al final elevar al exponente mas bajo que quede.
    float resultado = nodos[0]->coeficiente;
    int exponentePrevio = nodos[0]->exponente;

    for (int i = 1; i < indice; ++i) {
        for (int k = 0; k < exponentePrevio - nodos[i]->exponente; ++k) {
            resultado *= x;
        }
        resultado += nodos[i]->coeficiente;
        exponentePrevio = nodos[i]->exponente;
    }

    for (int k = 0; k < exponentePrevio; ++k) {
        resultado *= x;
    }

    return resultado;
}

/*****
* void recolectarEnOrdenInverso
******
* Recolecta los nodos del árbol en orden decreciente de exponente (mayor a menor),
* lo cual es útil para una evaluación eficiente del polinomio.
******
* Input:
* NodoArbol* nodo : nodo actual
* NodoArbol* (&arr)[100] : arreglo de punteros donde se almacenan los nodos
* int& indice : índice actual del arreglo
******
* Returns:
* void, no retorna valor
*****/
void PolinomioArbol::recolectarEnOrdenInverso(NodoArbol* nodo, NodoArbol* (&arr)[MAX_MONOMIOS], int& indice) const {
    if (!nodo) return;
    recolectarEnOrdenInverso(nodo->derecho, arr, indice);  // recorrer primero los exponentes mayores
    if (indice < MAX_MONOMIOS) {
        arr[indice++] = nodo;
    }
    recolectarEnOrdenInverso(nodo->izquierdo, arr, indice);
}
