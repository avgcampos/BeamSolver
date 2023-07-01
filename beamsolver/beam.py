#!/usr/bin/env python
# ==========================================================================#
#  This Python file is part of BeamSolver project                             #
#                                                                          #
#  The code is written by A. V. G. Campos                                  #
#                                                                          #
#  A github repository, with the most up to date version of the code,      #
#  can be found here:                                                      #
#     https://github.com/avgcampos/BeamSolver                                #
#                                                                          #
#  The code is open source and intended for educational and scientific     #
#  purposes only. If you use myfempy in your research, the developers      #
#  would be grateful if you could cite this.                               #
#                                                                          #
#  Disclaimer:                                                             #
#  The authors reserve all rights but do not guarantee that the code is    #
#  free from errors. Furthermore, the authors shall not be liable in any   #
#  event caused by the use of the program.                                 #
# ==========================================================================#
"""
BeamSolver -- Symbolic Solver to Elastic Beams
Copyright (C) 2023 Antonio Vinicius Garcia Campos
"""
# ==========================================================
from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import sympy as sb

x = sb.Symbol("x")
C0 = sb.Symbol("C0")
C1 = sb.Symbol("C1")
C2 = sb.Symbol("C2")
C3 = sb.Symbol("C3")


class NewBeam(ABC):
    """Class New Beam"""

    def __init__(self, Beam: apiBeam) -> None:
        self.beam = Beam
        L = 1.0
        E = 1.0
        I = 1.0
        load_list = [
            {"type": "apply", "order": 0, "value": 0.0, "begin": 0.0},
        ]

        bc_list = [
            {"type": "0", "dof": "v", "value": 0},
            {"type": "0", "dof": "s", "value": 0},
            {"type": "L", "dof": "M", "value": 0},
            {"type": "L", "dof": "V", "value": 0},
        ]

        self.beam.length = self.beam.setLength(L)
        self.beam.ei = self.beam.setEI(E, I)
        load, support = self.beam.setLoad(load_list)
        self.beam.load = load
        self.beam.support = support
        self.beam.bc = self.beam.getBoundCond(bc_list)

    def length(self, L: float):
        self.beam.length = self.beam.setLength(L)
        
    def thick(self, t_max: float,  t_min: float):
        self.beam.t_max = t_max
        self.beam.t_min = t_min
        
    def width(self, width: float):
        self.beam.b = width

    def EI(self, E: float, I: float):
        self.beam.i = I
        self.beam.ei = self.beam.setEI(E, I)
    
    def first_moment_of_area(self, Q: float):
        self.beam.q = Q

    def load(self, load_list: list):
        load, support = self.beam.setLoad(load_list)
        self.beam.load = load
        self.beam.support = support

    def bc(self, bc: list):
        self.beam.bc = self.beam.getBoundCond(bc)

    def shear(self):
        self.beam.shear = self.beam.getShear(self.beam.load)

    def bending(self):
        self.beam.bending = self.beam.getBending(self.beam.shear)

    def slope(self):
        self.beam.slope = self.beam.getSlope(self.beam.bending)

    def displacement(self):
        self.beam.displ = self.beam.getDisplacement(self.beam.slope)

    def constraint(self):
        L = self.beam.length
        V = self.beam.shear
        M = self.beam.bending
        s = self.beam.slope
        v = self.beam.displ

        return self.beam.setConstraintEq(self.beam.bc, V, M, s, v, L)

    def linsolve(self, consteqs):
        
        constraints = self.beam.getLinSolver(consteqs, self.beam.support)
        
        self.beam.shear_eval = (
            (self.beam.shear).subs(constraints)
        ).rewrite(sb.Piecewise)

        self.beam.bending_eval = (
            (self.beam.bending).subs(constraints)
        ).rewrite(sb.Piecewise)

        self.beam.slope_eval = (
            (1 / self.beam.ei * self.beam.slope).subs(constraints)
        ).rewrite(sb.Piecewise)

        self.beam.displ_eval = (
            (1 / self.beam.ei * self.beam.displ).subs(constraints)
        ).rewrite(sb.Piecewise)

    # def eval_constant(self, constraints):
    #     self.beam.shear_eval = (
    #         (self.beam.shear).subs(constraints)
    #     ).rewrite(sb.Piecewise)

    #     self.beam.bending_eval = (
    #         (self.beam.bending).subs(constraints)
    #     ).rewrite(sb.Piecewise)

    #     self.beam.slope_eval = (
    #         (1 / self.beam.ei * self.beam.slope).subs(constraints)
    #     ).rewrite(sb.Piecewise)

    #     self.beam.displ_eval = (
    #         (1 / self.beam.ei * self.beam.displ).subs(constraints)
    #     ).rewrite(sb.Piecewise)

    def getload(self):
        return self.beam.load

    def getbc(self):
        return self.beam.bc

    def getshear(self):
        return self.beam.shear_eval

    def getbending(self):
        return self.beam.bending_eval

    def getslope(self):
        return self.beam.slope_eval

    def getdisplacement(self):
        return self.beam.displ_eval

    def getshear_array(self, x_array):
        return (
            (sb.lambdify(x, self.beam.shear_eval, "numpy"))(x_array)
        ) * np.ones_like(x_array)

    def getbending_array(self, x_array):
        return (
            (sb.lambdify(x, self.beam.bending_eval, "numpy"))(x_array)
        ) * np.ones_like(x_array)

    def getslope_array(self, x_array):
        return (
            (sb.lambdify(x, self.beam.slope_eval, "numpy"))(x_array)
        ) * np.ones_like(x_array)

    def getdisplacement_array(self, x_array):
        return (
            (sb.lambdify(x, self.beam.displ_eval, "numpy"))(x_array)
        ) * np.ones_like(x_array)
        
    def stressxx(self, bending):
        
        x = np.linspace(0, self.beam.length, len(bending))
        y = np.linspace(self.beam.t_min, self.beam.t_max, len(bending))
        
        X, Y = np.meshgrid(x,y)
        SXX = -bending*Y/self.beam.i
        
        return X, Y, SXX


class apiBeam(ABC):
    """Class apiNewBeam"""

    @abstractmethod
    def setLength():
        pass

    @abstractmethod
    def setEI():
        pass

    @abstractmethod
    def setLoad():
        pass

    @abstractmethod
    def getBoundCond():
        pass

    @abstractmethod
    def setConstraintEq():
        pass

    @abstractmethod
    def getShear():
        pass

    @abstractmethod
    def getBending():
        pass

    @abstractmethod
    def getSlope():
        pass

    @abstractmethod
    def getDisplacement():
        pass

    @abstractmethod
    def getLinSolver():
        pass

    @abstractmethod
    def getNonLinSolver():
        pass


class BeamEB(apiBeam):
    """Class Beam Implement"""

    def setLength(L):
        return L

    def setEI(E, I):
        return E * I

    def getBoundCond(bc):
        return bc

    def setConstraintEq(bc_list, V, M, s, v, L):
        eqbc = []

        for itbc in range(len(bc_list)):
            if bc_list[itbc]["dof"] == "V":
                eqbc.append(
                    V.subs(x, bc_list[itbc]["begin"]) - bc_list[itbc]["value"]
                )

            elif bc_list[itbc]["dof"] == "M":
                eqbc.append(
                    M.subs(x, bc_list[itbc]["begin"]) - bc_list[itbc]["value"]
                )

            elif bc_list[itbc]["dof"] == "s":
                eqbc.append(
                    s.subs(x, bc_list[itbc]["begin"]) - bc_list[itbc]["value"]
                )

            elif bc_list[itbc]["dof"] == "v":
                eqbc.append(
                    v.subs(x, bc_list[itbc]["begin"]) - bc_list[itbc]["value"]
                )

        return eqbc

    def setLoad(load_list):
        load = []
        support = []
        for itl in range(len(load_list)):
            if load_list[itl]["type"] == "apply":
                if np.sign(load_list[itl]["value"]) == 1:
                    load.append("+")
                    load.append(
                        load_list[itl]["value"]
                        * sb.SingularityFunction(
                            x, load_list[itl]["begin"], load_list[itl]["order"]
                        )
                    )
                else:
                    load.append(
                        load_list[itl]["value"]
                        * sb.SingularityFunction(
                            x, load_list[itl]["begin"], load_list[itl]["order"]
                        )
                    )
            elif load_list[itl]["type"] == "support":
                sup_sym = sb.Symbol(load_list[itl]["value"])
                support.append(load_list[itl]["value"])
                load.append("+")
                load.append(
                    sup_sym
                    * sb.SingularityFunction(
                        x, load_list[itl]["begin"], load_list[itl]["order"]
                    )
                )

            else:
                pass

        load_str = " ".join(str(e) for e in load)
        load_sympy = sb.parsing.sympy_parser.parse_expr(load_str)

        support_constr = ", ".join(str(e) for e in support)

        return load_sympy, support_constr

    def getShear(load_sympy):
        return sb.integrate(load_sympy, x) + C0

    def getBending(shear):
        return sb.integrate(shear, x) + C1

    def getSlope(bending):
        return sb.integrate(bending, x) + C2

    def getDisplacement(slope):
        return sb.integrate(slope, x) + C3

    def getLinSolver(consteqs, support):
        symbols = sb.symbols("C0, C1, C2, C3, " + support)

        sol = sb.linsolve(consteqs, symbols)
        const_val = list(sol)[0]

        ss_str = []
        for e in symbols:
            ss_str.append(str(e))
        const = dict(zip(ss_str, list(const_val)))

        return const
