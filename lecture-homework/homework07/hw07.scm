(define (cddr s)
  (cdr (cdr s))
)


(define (cadr s)
  'YOUR-CODE-HERE
  (car (cdr s))
)

(define (caddr s)
  'YOUR-CODE-HERE
  (car (cddr s))
)


(define (sign num)
  'YOUR-CODE-HERE
  (cond
    ((= 0 num) '0)
    ((> 0 num) '-1)
    (else '1)
  )
)


(define (square x) (* x x))

(define (pow x y)
  'YOUR-CODE-HERE
  (if (= 1 y)
    x
    (if (even? y)
      (square (pow x (/ y 2)))
      (* x (pow x (- y 1)))
    )
  )
)


(define (unique s)
  'YOUR-CODE-HERE

  (define (find-item item sublst)
    (if (null? sublst)
      #f
      (if (eq? item (car sublst))
        #t
        (find-item item (cdr sublst))
      )
    )
  )

  (define (repeated x blst)
    (if (find-item x blst)
      blst
      (append blst (list x))
    )
  )

  (define (creat-new-list s alst)
    (if (null? s)
      alst
      (creat-new-list (cdr s) (repeated (car s) alst))
    )
  )

  (define lst '())

  (creat-new-list s lst)
)


(define (replicate x n)
  'YOUR-CODE-HERE
  (define (inner lst n)
    (if (= n 0)
      lst
      (inner (cons x lst) (- n 1))
    )
  )
  (inner '() n)
)


(define (accumulate combiner start n term)
  'YOUR-CODE-HERE
  (define (inner-accu combiner start n term)
    (if (= n 1)
      (term start)
      (combiner (term start) (inner-accu combiner (+ start 1) (- n 1) term))
    )
  )
  (combiner start (inner-accu combiner '1 n term))
)


(define (accumulate-tail combiner start n term)
  'YOUR-CODE-HERE
  (define (inner-accu combiner start n term result)
    (if (= n 0)
      result
      (inner-accu combiner (+ start 1) (- n 1) term (combiner result (term start)))
    )
  )
  (inner-accu combiner '1 n term start)
)


(define-macro (list-of map-expr for var in lst if filter-expr)
  'YOUR-CODE-HERE
  `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst))
)

(list-of (* x x) for x in '(3 4 5) if (odd? x))
