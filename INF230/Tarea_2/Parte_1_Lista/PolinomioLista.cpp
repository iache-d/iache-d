#include "PolinomioLista.hpp"

/*****
* Constructor Polinomio
******
* Inicializa un polinomio vacío
******
* Input:
* Ninguno
******
* Returns:
* void, constructor
*****/
Polinomio::Polinomio()
{
    cabeza = nullptr;
}

/*****
* Destructor ~Polinomio
******
* Libera toda la memoria utilizada por la lista enlazada del polinomio
******
* Input:
* Ninguno
******
* Returns:
* void, destructor
*****/
Polinomio::~Polinomio()
{
    liberar();
}

/*****
* void insertarMonomio
******
* Inserta un monomio (exponente y coeficiente) en la posición correspondiente de la lista ordenada.
* Si ya existe un monomio con ese exponente, actualiza su coeficiente.
******
* Input:
* int exponente : exponente del monomio
* int coeficiente : coeficiente del monomio
******
* Returns:
* void, no retorna valor
*****/
void Polinomio::insertarMonomio(int exponente, int coeficiente)
{
    if (coeficiente == 0)
        return;

    Monomio *nuevo = new Monomio(exponente, coeficiente);

    if (!cabeza || exponente < cabeza->exponente)
    {
        nuevo->siguiente = cabeza;
        cabeza = nuevo;
        return;
    }

    Monomio *actual = cabeza;
    Monomio *anterior = nullptr;

    while (actual && actual->exponente < exponente)
    {
        anterior = actual;
        actual = actual->siguiente;
    }

    if (actual && actual->exponente == exponente)
    {
        actual->coeficiente = coeficiente;
        delete nuevo;
    }
    else
    {
        nuevo->siguiente = actual;
        anterior->siguiente = nuevo;
    }
}

/*****
* int obtenerCoeficiente
******
* Retorna el coeficiente asociado al exponente dado. Si no existe, retorna 0.
******
* Input:
* int exponente : exponente que se desea consultar
******
* Returns:
* int, coeficiente correspondiente (o 0 si no existe)
*****/
int Polinomio::obtenerCoeficiente(int exponente) const
{
    Monomio *actual = cabeza;
    while (actual)
    {
        if (actual->exponente == exponente)
            return actual->coeficiente;
        if (actual->exponente > exponente)
            break;
        actual = actual->siguiente;
    }
    return 0;
}

/*****
* float evaluar
******
* Evalúa el polinomio para un valor dado de x.
******
* Input:
* float x : valor en el que se desea evaluar el polinomio
******
* Returns:
* float, resultado de la evaluación
*****/
float Polinomio::evaluar(float x) const
{
    // Paso 1: Invertimos la lista enlazada original
    Monomio* invertida = nullptr;
    Monomio* actual = cabeza;

    while (actual)
    {
        Monomio* copia = new Monomio(actual->exponente, actual->coeficiente);
        copia->siguiente = invertida;
        invertida = copia;
        actual = actual->siguiente;
    }

    // Paso 2: Aplicamos Horner
    float resultado = 0;
    int exponentePrevio = 0;
    actual = invertida;

    if (actual)
    {
        resultado = actual->coeficiente;
        exponentePrevio = actual->exponente;
        actual = actual->siguiente;
    }

    while (actual)
    {
        int diferencia = exponentePrevio - actual->exponente;

        // Multiplicamos resultado por x ^ diferencia
        for (int i = 0; i < diferencia; ++i)
        {
            resultado *= x;
        }

        resultado += actual->coeficiente;
        exponentePrevio = actual->exponente;
        Monomio* temp = actual;
        actual = actual->siguiente;
        delete temp; // liberamos memoria de la lista invertida
    }

    // Finalmente multiplicamos por x^exponentePrevio si no era 0
    for (int i = 0; i < exponentePrevio; ++i)
    {
        resultado *= x;
    }

    delete invertida; // liberamos el último nodo restante

    return resultado;
}


/*****
* void liberar
******
* Libera toda la memoria dinámica usada por los nodos del polinomio.
******
* Input:
* Ninguno
******
* Returns:
* void, no retorna valor
*****/
void Polinomio::liberar()
{
    while (cabeza)
    {
        Monomio *tmp = cabeza;
        cabeza = cabeza->siguiente;
        delete tmp;
    }
}
