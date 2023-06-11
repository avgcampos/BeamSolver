from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import sys

x = Symbol('x')
C0 = Symbol('C0')
C1 = Symbol('C1')
C2 = Symbol('C2')
C3 = Symbol('C3')
# EI = Symbol('EI')

EI = 1.0
comp = 1.0

xx = np.linspace(0, comp, 500)

q0 = -1.0
pos = 0.0

load =  q0*SingularityFunction(x, pos, 0) #- q0*SingularityFunction(x, 0.5, 0)
load_piec = load.rewrite(Piecewise)
load_vector = lambdify(x, load_piec, "numpy")

V = integrate(load, x) + C0
M = integrate(V, x) + C1
t = integrate(M, x) + C2
v = integrate(t, x) + C3

# print(v)

eq = [M.subs(x, comp), v.subs(x, 0), M.subs(x, 0), v.subs(x, comp)]

print(eq)
 
# sys.exit()

sol = linsolve(eq, C0, C1, C2, C3)

const_val = list(sol)[0]

print(const_val)

# sys.exit()

V_array = (V.subs({C0: const_val[0]})).rewrite(Piecewise)
M_array = (M.subs({C0: const_val[0], C1: const_val[1]})).rewrite(Piecewise)
t_array = (1/EI*t.subs({C0: const_val[0], C1: const_val[1], C2: const_val[2]})).rewrite(Piecewise)
v_array = (1/EI*v.subs({C0: const_val[0], C1: const_val[1], C2: const_val[2], C3: const_val[3]})).rewrite(Piecewise)

# print(V_array)
# print(M_array)
# print(t_array)
# print(v_array)

V_array_numpy = lambdify(x, V_array, "numpy")
M_array_numpy = lambdify(x, M_array, "numpy")
t_array_numpy = lambdify(x, t_array, "numpy")
v_array_numpy = lambdify(x, v_array, "numpy")


plt.close('all')
plt.figure()
plt.subplot(511)
plt.plot(xx,load_vector(xx),'r')
plt.grid('on')
plt.subplot(512)
plt.plot(xx,V_array_numpy(xx),'g')
plt.grid('on')
plt.subplot(513)
plt.plot(xx,M_array_numpy(xx),'b')
plt.grid('on')
plt.subplot(514)
plt.plot(xx,t_array_numpy(xx),'m')
plt.grid('on')
plt.subplot(515)
plt.plot(xx,v_array_numpy(xx),'k')
plt.grid('on')
plt.show()