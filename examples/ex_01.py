# BeamSolver Examples
# ---------------------------------------------------
# Ex: 01: Viga bi-apoiada c/ carga distribuida
# Antonio Campos 2023
#
#      |vvvvvvvvvvvvvvvvvvvvvvvvvvv| q(x) = -10 [N/mm]
#       ___________________________
#      /\                         /\
#      @x = 0                      @x = L = 1000 [mm]
#
# E = 200E3 [MPa]
# I = 65E6  [mm4]
# ---------------------------------------------------
from beamsolver import NewBeam, BeamEB

import numpy as np
import matplotlib.pyplot as plt

beam = NewBeam(BeamEB)

L = 1000
E = 200E6
I = 65E6

beam.length(L)
beam.EI(E, I)

load_1 = {
    'type': 'apply',
    'order': 0,
    'value': -10.0,
    'begin': 0.0*L
}

bc_1 = {
    'dof': 'v',
    'begin': 0,
    'valeu': 0.0,
}

bc_2 = {
    'dof': 'v',
    'begin': 0,
    'valeu': 0.0,
}

bc_3 = {
    'dof': 'v',
    'begin': L,
    'valeu': 0.0,
}

bc_4 = {
    'dof': 'M',
    'begin': L,
    'valeu': 0.0,
}


beam.load([load_1])
beam.bc([bc_1, bc_2, bc_3, bc_4])

get_load = beam.getload()

print(get_load)






