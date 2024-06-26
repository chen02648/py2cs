from env import *
from parse import parse_lisp

class Function(object): # 函數定義
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, *args): 
        if len(args) != len(self.params):
            raise Exception(f'({self.params}) 和 {args} 參數數量不符!')
        fenv = Env(zip(self.params, args), self.env)
        return evaluate(self.body, fenv)

# LISP (Scheme) 解釋器
def evaluate(code, env):
    if isinstance(code, list):
        if code[0] == 'define': # 定義新變數
            _, var, value = code
            env[var] = evaluate(value, env)
        elif code[0] == 'lambda':
            _, params, body = code
            return Function(params, body, env)
        elif code[0] == 'if':             # (if cond exp1 exp2)
            (_, cond, exp1, exp2) = code
            exp = exp1 if evaluate(cond, env) else exp2
            return evaluate(exp, env)
        elif code[0] == 'set!':           # (set! var exp)
            (_, var, exp) = code
            env.findEnv(var)[var] = evaluate(exp, env)
        elif code[0] == 'quote':          # (quote exp)
            (_, exp) = code
            return exp # 直接傳回 exp，不執行
        else: 
            # 函數調用
            func = evaluate(code[0], env)
            args = [evaluate(arg, env) for arg in code[1:]]
            return func(*args)
    elif isinstance(code, Symbol) and (env.findEnv(code)):
        # 變數引用
        return env.findVar(code)
    else:
        # 常數
        return code

def test(prog, answer):
    global gEnv
    blocks = prog.split(";")
    print(f"{blocks}")
    for block in blocks:
        code = parse_lisp(block)
        # print("code=", code)
        result = evaluate(code, gEnv)
    print(f"  {result}==?{answer}", end=" ")
    if result == answer:
        print("✓")
    else:
        print("⨉")


# 測試 Scheme (lisp 方言) 的解釋器
if __name__ == "__main__":
    test("((lambda (x y) (+ x y)) 3 4)", 7) # 定義一個 lambda 函數並調用
    test("(define add (lambda (x y) (+ x y)));(add 3 4)", 7) # 定義一個有名稱的函數並調用
    test("(if (> 6 5) (+ 1 1) (+ 2 2))", 2),
    test("(if (< 6 5) (+ 1 1) (+ 2 2))", 4),
    test("(begin (define x 1) (set! x (+ x 1)) (+ x 1))", 3)
    test("(define twice (lambda (x) (* 2 x)))", None), ("(twice 5)", 10)
    test("(define compose (lambda (f g) (lambda (x) (f (g x)))))", None)
    test("((compose list twice) 5)", [10])
    test("(define repeat (lambda (f) (compose f f)))", None),
    test("((repeat twice) 5)", 20), ("((repeat (repeat twice)) 5)", 80)
    test("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))", None)
    test("(fact 3)", 6)
    test("(fact 10)", 3628800)
    test("(define abs (lambda (n) ((if (> n 0) + -) 0 n)))", None)
    test("(abs -3)", 3)
    test("(abs 0)", 0) # fail
    test("(abs 3)", 3)
    test("(list (abs -3) (abs 0) (abs 3))", [3, 0, 3])
    test("""
    (define combine (lambda (f)
    (lambda (x y)
      (if (null? x) (quote ())
          (f (list (car x) (car y))
             ((combine f) (cdr x) (cdr y)))))))
    """, None)
    test("(define zip (combine cons))", None)
    test("(zip (list 1 2 3 4) (list 5 6 7 8))", [[1, 5], [2, 6], [3, 7], [4, 8]])
    test("""(define riff-shuffle (lambda (deck) (begin
    (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))""", None)
    test("(riff-shuffle (list 1 2 3 4 5 6 7 8))", [1, 5, 2, 6, 3, 7, 4, 8])
    test("((repeat riff-shuffle) (list 1 2 3 4 5 6 7 8))",  [1, 3, 5, 7, 2, 4, 6, 8])
    test("(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))", [1,2,3,4,5,6,7,8])
