from beamsolver import BeamEB, NewBeam

import numpy as np
import matplotlib.pyplot as plt

import sys

nbeam = NewBeam(BeamEB)

L = 1.0
E = 1.0
I = 1.0

nbeam.length(L)
nbeam.EI(E, I)

xx = np.linspace(0, L, 500)

l1 = {
    'type': 'apply', # rem, sup
    'order': 0,
    'value': 1.0,
    'begin': 0.0*L
    }

l2 = {
    'type': 'apply', # rem, sup
    'order': 0,
    'value': -1.0,
    'begin': 0.5*L
    }

l3 = {
    'type': 'apply', # rem, sup
    'order': -1,
    'value': 1.0,
    'begin': 3/4*L
    }


r1 = {
    'type': 'support',
    'order': -1,
    'value': 'R1y',
    'begin': 1/4*L
    }


# l2 = {
#     'type': 'remove', # rem, sup
#     'order': -1,
#     'value': +1.0,
#     'begin': 0.25*L
#     }


# l3 = {
#     'type': 'apply', # rem, sup
#     'order': -1,
#     'value': -1.0,
#     'begin': 0.75*L
#     }


bc1 = {
    'begin': L, # 'L'
    'dof': 'v',
    'value': 0,
    }


bc2 = {
    'begin': L, # 'L'
    'dof': 's',
    'value': 0,
    }


bc3 = {
    'begin': 0, # 'L'
    'dof': 'M',
    'value': -1.0,
    }


bc4 = {
    'begin': 0, # 'L'
    'dof': 'V',
    'value': 0.0,
    }


rs1 = {
    'dof': 'v',
    'value': 0,
    'begin': 1/4*L,
    }


nbeam.load([l1, l2, l3, r1])

nbeam.bc([bc1, bc2, bc3, bc4, rs1])

loadsf = nbeam.getload()

print(loadsf)

# sys.exit()

import sympy as sb
x = sb.Symbol('x')

xx = np.linspace(0, L, 500)

load_piecewise = loadsf.rewrite(sb.Piecewise)
load_vector = sb.lambdify(x, load_piecewise, "numpy")

plt.figure()
plt.plot(xx,load_vector(xx))
plt.grid('on')
plt.show()

sys.exit()

nbeam.shear()
# print(nbeam.getshear())

nbeam.bending()
# print(nbeam.getbending())

nbeam.slope()
# print(nbeam.getslope())

nbeam.displacement()
# print(nbeam.getdisplacement())

const = nbeam.constraint()

# print(const)

sol = nbeam.linsolve(const)

# print(sol)

nbeam.eval_constant(sol)

beam_shear = nbeam.getshear_array(xx)
beam_bending = nbeam.getbending_array(xx)
beam_slope = nbeam.getslope_array(xx)
beam_displ = nbeam.getdisplacement_array(xx)

plt.close('all')
plt.figure()
plt.subplot(411)
plt.title('Cortante')
plt.plot(xx,beam_shear,'g')
plt.grid('on')
plt.subplot(412)
plt.title('Momento')
plt.plot(xx,beam_bending,'b')
plt.grid('on')
plt.subplot(413)
plt.title('Rotação')
plt.plot(xx,beam_slope,'m')
plt.grid('on')
plt.subplot(414)
plt.title('Deslocamento')
plt.plot(xx,beam_displ,'k')
plt.grid('on')
plt.show()