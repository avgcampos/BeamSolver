from sympy import *
x, y, z = symbols("x y z")

# expr = cos(x) + 1

# print(expr.subs(x, 0))

def f(x):
    return 2*x

print(f(1))

def diff_f(func):
    return diff(func, x, 1)

print(diff_f(f(1)))