(defpackage #:secdm
  (:use #:cl)
  (:export))
(in-package #:secdm)

(defstruct env
  (type :lex :type (member :lex :dyn))
  (parent nil :type env)
  (table (make-hash-table)))

(defstruct (vm (:constructor make-vm*))
  (debug-p nil)
  s e c d)

(defmethod print-object ((vm vm) stream)
  (format stream
          "VM:~%  S: ~s~%  E: ~s~%  C: ~s~%  D: ~s~%"
          (vm-s vm) (vm-e vm) (vm-c vm) (vm-d vm)))

(defun run-1 (vm)
  (when (vm-debug-p vm)
    (format t "~s" vm))
  (when (null (vm-c vm))
    (return-from run-1 nil))
  (let ((op (pop (vm-c vm))))
    (assert (listp op))
    (let ((name (car op))
          (args (cdr op)))
      (assert (symbolp name))
      (apply name vm args)
      t)))

(defpackage #:secdm/op
  (:use))

(defpackage #:secdm/symbol
  (:use #:secdm/op))

(defun ensure-secdm-package (code)
  (cond ((or (null code)
             (numberp code))
         code)
        ((symbolp code) (intern (symbol-name code) :secdm/symbol))
        ((consp code) (cons (ensure-secdm-package (car code))
                            (ensure-secdm-package (cdr code))))))

(defun make-vm (debug-p code)
  (let ((code (ensure-secdm-package code)))
    (make-vm* :c code :debug-p debug-p)))

(defmacro defop (name (&rest args) &body body)
  (let ((fn-name (intern (symbol-name name) :secdm/op)))
    `(progn
       (defun ,fn-name ,args
         ,@body)
       (export ',fn-name :secdm/op))))

(defop ldc (vm n)
  (push n (vm-s vm)))