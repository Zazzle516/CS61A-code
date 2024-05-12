(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  (map
    (lambda (x)
      (append (list first) x)
    )
    rests
  )  
)

(define (zip pairs)
  (define (helper lst first second)
    (if (null? lst)
      (list first second)
      (helper (cdr lst) (append first (list (car (car lst)))) (append second (list (car (cdr (car lst))))))
    )
  )
  (helper pairs nil nil)
)

;; Problem 16
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 16
  (define (helper index lst ans)
    (if (null? lst)
      ans
      (helper
        (+ 1 index)
        (cdr lst)
        (append ans
          (list (list index (car lst)))
        )
      )
    )
  )
  (helper 0 s nil)
  ; END PROBLEM 16
)


;; Problem 17
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 17
  (if (eq? 0 total)
    (list nil)
    (if (null? denoms)
      nil
      (if (<= (car denoms) total)
        (append
          (cons-all (car denoms) (list-change (- total (car denoms)) denoms))
          (list-change total (cdr denoms))
        )
        (list-change total (cdr denoms))
      )
    )
  )
  ; END PROBLEM 17
)


;; Problem 18
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         expr
        )

        ((quoted? expr)
          ; double quote
         expr
        )
        
        ((or (lambda? expr)
             (define? expr))
          (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
              (cons form (cons params (map let-to-lambda body)))
          )
        )

        ((let? expr)
          (let ((values (cadr expr))
               (body   (cddr expr)))
            (define formals (car (zip values)))
            (define value (cadr (zip values)))

            (append
              (cons (cons 'lambda (cons formals (map let-to-lambda body))) nil)
              (map let-to-lambda value)
            )
          )
        )

        (else
          ; exec body (operator operands)
          ; !every operand need to recursive compute!
          ; (cons (car expr) (cons (map let-to-lambda (cdr expr)) nil))
          ; recursion will ensure the structure, don't need extra (cons ..)
          (cons (car expr) (map let-to-lambda (cdr expr)))
        )
  )
)