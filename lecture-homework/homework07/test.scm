(define (accumulate combiner start n term)
  'YOUR-CODE-HERE
  (define (inner-accu combiner start n term result)
    (if (= n 1)
      result
      (inner-accu combiner (+ start 1) (- n 1) term (combiner result (term start)))
    )
  )
  (inner-accu combiner '1 n term start)
)