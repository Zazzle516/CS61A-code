
(define-macro (def func args body)
  ; (cons func (cons args (cons (cons body) nil)))
  `(define ,(cons func args) ,body)
)


(define (map-stream f s)
    (if (null? s)
    	nil
    	(cons-stream (f (car s)) (map-stream f (cdr-stream s))))
)


(define all-three-multiples
  (map-stream (lambda (x) (+ x 3)) (cons-stream 0 all-three-multiples))
)


(define (compose-all funcs)
  ; (define (place-taker x)
  ;   x
  ; )

  ; (if (null? funcs)
  ;   place-taker
  ;   (begin
  ;     ; (car funcs)
  ;     (display (car funcs))
  ;     (compose-all (cdr funcs))
  ;     (car funcs)
  ;   )
  ; )
  (if (null? funcs)
      (lambda (x) x)

      (lambda (x) (
        (compose-all (cdr funcs))
        ((car funcs) x))
      )
  )
)


; (define (partial-sums stream)
;   'YOUR-CODE-HERE
;   (define (helper current-ans input-stream)
;     (+ (car-stream input-stream) current-ans)
;     (helper (+ (car-stream input-stream) current-ans) (cdr-stream input-stream))
;   )
;   (helper 0 stream)
; )


(define (partial-sums stream)
  (define (helper current-ans input-stream)
    (if (null? input-stream)
      nil
      (cons-stream
        (+ current-ans (car input-stream))
        (helper (+ current-ans (car input-stream)) (cdr-stream input-stream))
      )
    )
  )
  (helper 0 stream)
)

