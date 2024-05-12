(define (helper curr num s)
    (if (and (not (null? s)) (= curr (car s)))
        (helper curr (+ num 1) (cdr-stream s))
        (list curr num)
    )
)

(define (next s curr)
    (if (null? s)
        nil
        (if (= (car s) curr)
            (next (cdr-stream s) curr)
            s
        )
    )
)

(define (rle s)
  'YOUR-CODE-HERE
  (if (null? s) nil
    (cons-stream (helper (car s) 0 s) (rle (next s (car s))))
  )
)


(define (group-process curr input-stream group-ans)
    (if (null? input-stream)
        group-ans
        (if (> curr (car input-stream))
            group-ans
            (group-process (car input-stream) (cdr-stream input-stream) (append group-ans (list (car input-stream))))
        )
    )
)


(define (input-rest input curr)
    (if (null? input)
        nil
        (if (> curr (car input))
            input
            (input-rest (cdr-stream input) (car input))
        )
    )
)


(define (group-by-nondecreasing s)
    (if (null? s)
        nil
        (cons-stream (group-process (car s) (cdr-stream s) (list (car s))) (group-by-nondecreasing (input-rest s (car s))))
    )
)


(define finite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 3
                (cons-stream 1
                    (cons-stream 2
                        (cons-stream 2
                            (cons-stream 1 nil)))))))
)


(define infinite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 2
                infinite-test-stream)))
)
