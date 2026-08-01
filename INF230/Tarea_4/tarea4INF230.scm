;;; apply-func-expt
;;;
;;; Eleva cada numero de la lista l al exponente i y aplica la operacion f entre
;;; todos los resultados. Se descartan los elementos que producirian un error
;;; matematico: 0 elevado a un exponente negativo, y un 0 usado como divisor.

(define (apply-func-expt f i l)

  ;; Un elemento se descarta si elevarlo a i, o usarlo como divisor, no esta definido.
  (define (descartar? x)
    (or (and (= x 0) (< i 0))
        (and (eq? f /) (= x 0))))

  ;; Elemento neutro de la operacion. Tambien valida que f sea un operador aceptado.
  (define identidad
    (cond
      [(eq? f +) 0]
      [(eq? f -) 0]
      [(eq? f *) 1]
      [(eq? f /) 1]
      [else (error "Operador no válido")]))

  ;; Potencias de los elementos validos, conservando el orden original.
  ;; Recursiva de cola: acumula al reves y revierte al terminar.
  (define (potencias lst acc)
    (cond
      [(null? lst) (reverse acc)]
      [(descartar? (car lst)) (potencias (cdr lst) acc)]
      [else (potencias (cdr lst) (cons (expt (car lst) i) acc))]))

  ;; Pliegue por la izquierda, recursivo de cola.
  (define (iter lst acc)
    (if (null? lst)
        acc
        (iter (cdr lst) (f acc (car lst)))))

  (let ([vals (potencias l '())])
    (cond
      ;; Sin elementos validos: se devuelve el neutro de la operacion.
      [(null? vals) identidad]

      ;; Un solo elemento: Scheme define (+ a) = (* a) = a, (- a) = -a y (/ a) = 1/a.
      ;; Aplicar la operacion sobre el neutro reproduce exactamente esos cuatro casos.
      [(null? (cdr vals)) (f identidad (car vals))]

      ;; Dos o mas elementos: se parte del primero y se pliega el resto, que es lo que
      ;; significa aplicar f entre todos los resultados. Partir del neutro seria
      ;; incorrecto para - y /, porque (- a b c) es a-b-c y no 0-a-b-c.
      [else (iter (cdr vals) (car vals))])))
