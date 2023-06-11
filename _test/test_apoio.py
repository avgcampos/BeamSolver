from sympy import *
import numpy as np
import matplotlib.pyplot as plt

x = Symbol('x')
C0 = Symbol('C0')
C1 = Symbol('C1')

#add suport
Ry = Symbol('Ry')

comp = 1.0

xx = np.linspace(0, comp, 500)

q0 = -1.0
pos = 0.5*comp

load =  q0*SingularityFunction(x, pos, -1) + Ry*SingularityFunction(x, 3*comp/4, -1) #- q0*SingularityFunction(x, 0.5, 0)
load_piec = load.rewrite(Piecewise)
load_vector = lambdify(x, load_piec, "numpy")

V = integrate(load, x) + C0

# print(V) 

M = integrate(V, x) + C1

# print(M.subs(x, 1))

eq = [V.subs(x, comp), M.subs(x, 0), M.subs(x, comp)] # from bc

# print(eq)

sol = linsolve(eq, C0, C1, Ry)

const_val = list(sol)[0]

# print(const_val)

V_array = (V.subs({Ry: const_val[2], C0: const_val[0]})).rewrite(Piecewise)
M_array = (M.subs({Ry: const_val[2], C0: const_val[0], C1: const_val[1]})).rewrite(Piecewise)

print(V_array)
print(M_array)

V_array_numpy = lambdify(x, V_array, "numpy")
M_array_numpy = lambdify(x, M_array, "numpy")

plt.close('all')
plt.figure()
plt.subplot(311)
plt.plot(xx,load_vector(xx),'r')
plt.grid('on')
plt.subplot(312)
plt.plot(xx,V_array_numpy(xx),'g')
plt.grid('on')
plt.subplot(313)
plt.plot(xx,M_array_numpy(xx),'b')
plt.grid('on')
plt.show()