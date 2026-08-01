#ifndef POLINOMIO_LISTA_HPP
#define POLINOMIO_LISTA_HPP

#include <iostream>


/*****
* struct Monomio
******
* Nodo de la lista enlazada que representa un monomio del polinomio.
******
* Input:
* int exp : Exponente del monomio
* int coef : Coeficiente del monomio
******
* Returns:
* Constructor, inicializa el nodo con los valores entregados y puntero siguiente en nullptr
*****/
struct Monomio
{
    int exponente;
    int coeficiente;
    Monomio *siguiente;

    Monomio(int exp, int coef) : exponente(exp), coeficiente(coef), siguiente(nullptr) {}
};

/*****
* class Polinomio
******
* Clase que representa un polinomio como una lista enlazada ordenada de monomios.
* Provee operaciones para insertar, evaluar y obtener coeficientes.
*****/
class Polinomio
{
private:
    Monomio *cabeza;

public:
    /*****
    * Constructor Polinomio
    ******
    * Inicializa un polinomio vacío (lista enlazada vacía)
    ******
    * Input:
    * Ninguno
    ******
    * Returns:
    * void, constructor
    *****/
    Polinomio();

    /*****
    * Destructor ~Polinomio
    ******
    * Libera toda la memoria dinámica utilizada por el polinomio
    ******
    * Input:
    * Ninguno
    ******
    * Returns:
    * void, destructor
    *****/
    ~Polinomio();

    /*****
    * void insertarMonomio
    ******
    * Inserta o actualiza un monomio en el polinomio. La lista se mantiene ordenada por exponente.
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
    * Evalúa el polinomio para un valor de x dado.
    ******
    * Input:
    * float x : valor en el cual se evaluará el polinomio
    ******
    * Returns:
    * float, resultado numérico de la evaluación
    *****/
    float evaluar(float x) const;

    /*****
    * void liberar
    ******
    * Libera toda la memoria dinámica de la lista enlazada.
    ******
    * Input:
    * Ninguno
    ******
    * Returns:
    * void, no retorna valor
    *****/
    void liberar();
};

#endif
