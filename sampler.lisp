(script "Sampler"
  (enter "Sampler")
  (push-fresh-accumulator)
  (call Stuff 
    (✓ (prefetch 1)
       (peek-end
	 (✓ (accept-and-append)
	   (send-accumulator "✓"))
	 (✗ (send-string "" "✗") )))
    (✗ (send-string "" "✗") ))
  (pop-accumulator)
  (exit "Sampler"))

(script "Stuff"
  (enter "Stuff")
  (push-fresh-accumulator)
  (cycle
    (prefetch 11)
    (peek "Hello World"
      (✓ (call Hello
	   (✓ (continue))
	   (✗ (send-string "" "✗") 
	      (break))))
      (✗ (peek-end
	   (✓ (send-accumulator "✓") 
	      (break))
  	   (✗ (accept-and-append)
	      (continue))))))
  (pop-accumulator)
  (exit "Stuff"))


(script "Hello"
  (enter "Hello")
  (push-fresh-accumulator)
  (prefetch 11)
  (peek "Hello World"
    (✓ (accept-and-append)
       (send-accumulator "✓"))
    (✗ (send-string "" "✗")))
  (pop-accumulator)
  (exit "Hello"))
