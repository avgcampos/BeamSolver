from sympy import *
import numpy as np
import matplotlib.pyplot as plt

x = Symbol('x')

xx = np.linspace(0,4,500)

# expr = x**2 + x
# print(expr.evalf(subs={x: 2}))
# print(expr)
# print(2*expr)
# print(diff(expr, x, 1))
# print(integrate(expr, x))
# print(solve(expr, x))

# load_1 = 10*((x)**)  # *(xx>0) # -10*SingularityFunction(x, 0, 0)

load_2 = 10*SingularityFunction(x, 2, 0) # - 10*SingularityFunction(x, 2, 1)
load_piec = load_2.rewrite(Piecewise)
load_vector = lambdify(x, load_piec, "numpy")

load_int = integrate(load_2, x)
load_piec_int = load_int.rewrite(Piecewise)
load_vector_int = lambdify(x, load_piec_int, "numpy")

# plt.plot(xx,load_vector(xx),xx,load_vector_int(xx))
# plt.show()
