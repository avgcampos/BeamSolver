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
BeamSolver -- Symbolic Solver to Elastic Beam
Copyright (C) 2023 Antonio Vinicius Garcia Campos
"""
# ==========================================================
from __future__ import absolute_import

from . import beam, version
from .beam import BeamEB, NewBeam

# ==========================================================
__author__ = "Antonio Vinicius Garcia Campos"
__copyright__ = "Copyright @ 2023, Antonio Vinicius Garcia Campos"
__credits__ = ["Antonio Vinicius Garcia Campos"]
__license__ = "GPL-3.0"
__status__ = "Development"
__website__ = "https://github.com/avgcampos/BeamSolver"
__version__ = version.__version__
# ==========================================================
__all__ = ["__version__"]
# ==========================================================
