#!/usr/bin/env guile
!#
;;; Minimal agent implementation in Guile Scheme

(use-modules (ice-9 format)
             (ice-9 readline)
             (web client)
             (json)
             (srfi srfi-1))

;; Tool definition
(define (make-tool name description parameters function)
  `((name . ,name)
    (description . ,description)
    (parameters . ,parameters)
    (function . ,function)))

;; Tool registry
(define *tools* '())

(define (register-tool! tool)
  (set! *tools* (cons tool *tools*)))

;; Register basic tools
(register-tool!
 (make-tool
  "read_file"
  "Read contents of a file"
  '((type . "object")
    (properties . ((path . ((type . "string")))))
    (required . #("path")))
  (lambda (path)
    (call-with-input-file path
      (lambda (port)
        (get-string-all port))))))

;; Main REPL
(define (agent-repl)
  (activate-readline)
  (format #t "Terminal Agent (Guile)~%")
  (let loop ()
    (display "> ")
    (let ((input (readline)))
      (unless (member input '("quit" "exit"))
        ;; Process with LLM here
        (format #t "Processing: ~a~%" input)
        (loop)))))

(agent-repl)
