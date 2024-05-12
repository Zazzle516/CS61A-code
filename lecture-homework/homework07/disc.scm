(define (insert n lst)
    (define (copy-lst n result lst)
        (if (null? lst)
            result
            (if (>= n (car lst))
                (if (<= n (car (cdr lst)))
                    (copy-lst n (cons result (cons n nil)) (cdr lst))
                    (copy-lst n (cons result (cons (car lst) nil)) (cdr lst))
                )
                (copy-lst n (cons result (cons (car lst) nil)) (cdr lst))
            )
        )
    )
    (copy-lst n () lst)
)