from beamsolver import BeamEB, NewBeam

import numpy as np
import matplotlib.pyplot as plt


nbeam = NewBeam(BeamEB)

L = 1

nbeam.length(L)

nbeam.EI(1, 1)

xx = np.linspace(0, L, 500)

l1 = {
    'type': 'apply', # rem, sup
    'order': -1,
    'value': -1.0,
    'begin': 0.25*L
    }

l2 = {
    'type': 'remove', # rem, sup
    'order': -1,
    'value': +1.0,
    'begin': 0.25*L
    }


l3 = {
    'type': 'apply', # rem, sup
    'order': -1,
    'value': -1.0,
    'begin': 0.75*L
    }

bc1 = {
    'type': '0', # 'L'
    'dof': 'v',
    'value': 0,
    }


bc2 = {
    'type': 'L', # 'L'
    'dof': 'v',
    'value': 0,
    }

bc3 = {
    'type': '0', # 'L'
    'dof': 'M',
    'value': 0,
    }

bc4 = {
    'type': 'L', # 'L'
    'dof': 'M',
    'value': 0,
    }

nbeam.load([l1, l3])

nbeam.bc([bc1, bc2, bc3, bc4])

loadsf = nbeam.getload()

# print(loadsf)

# x = sb.Symbol('x')

# xx = np.linspace(0, 1.0, 500)

# load_piecewise = loadsf.rewrite(sb.Piecewise)
# load_vector = sb.lambdify(x, load_piecewise, "numpy")

# plt.figure()
# plt.plot(xx,load_vector(xx))
# plt.grid('on')
# plt.show()

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

sol = nbeam.solve(const)

nbeam.eval_constant(sol)

beam_shear = nbeam.getshear_array(xx)
beam_bending = nbeam.getbending_array(xx)
beam_slope = nbeam.getslope_array(xx)
beam_displ = nbeam.getdisplacement_array(xx)


plt.close('all')
plt.figure()
plt.subplot(411)
plt.plot(xx,beam_shear,'g')
plt.grid('on')
plt.subplot(412)
plt.plot(xx,beam_bending,'b')
plt.grid('on')
plt.subplot(413)
plt.plot(xx,beam_slope,'m')
plt.grid('on')
plt.subplot(414)
plt.plot(xx,beam_displ,'k')
plt.grid('on')
plt.show()