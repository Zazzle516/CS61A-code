;Definitions
(define (square x) (* x x))

(define (average x y) (/ (+ x y) 2))

; else-branch write in the if-statement
(define (abs x)
    (if (< x 0)
        (- x)
    x )
)

(define sum-square
    (lambda (x y) (+ (square x) (square y)))
)

(define (fib x)
    (cond ((= x 0) 0)
        ((= x 1) 1)
        (else (+ (fib (- x 1)) (fib (- x 2))))
    )
)

; cons = construction
(define a (cons 1 (cons 2 (cons 3 nil))))

; Higher Order Function
(define (sum-while starting-x while-condition add-to-total update-x)
    `(begin
        (define (f x total)
            (if ,while-condition
                (f ,update-x (+ total ,add-to-total))
                total
            )
        )
        (f ,starting-x 0)
    )
)

(define (factorial x)
    (if (= x 1)
        1
        ;(* x (factorial (- x 1)))
        #f
    )
)

factorial(3)