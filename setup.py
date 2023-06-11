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
#  event caused by the use of the program.                                #
#==========================================================================#
"""
#==========================================================================#

             ____                        _____       _                
            |  _ \                      / ____|     | |               
            | |_) | ___  __ _ _ __ ___ | (___   ___ | |_   _____ _ __ 
            |  _ < / _ \/ _` | '_ ` _ \ \___ \ / _ \| \ \ / / _ \ '__|
            | |_) |  __/ (_| | | | | | |____) | (_) | |\ V /  __/ |   
            |____/ \___|\__,_|_| |_| |_|_____/ \___/|_| \_/ \___|_|   
                                                                    
                                                           
~~~              BeamSolver -- Symbolic Solver to Elastic Beam           ~~~
~~~                     COMPUTATIONAL ANALYSIS PROGRAM                   ~~~
~~~                    PROGRAMA DE ANÁLISE COMPUTACIONAL                 ~~~
~~~             Copyright (C) 2022 Antonio Vinicius Garcia Campos        ~~~
#==========================================================================#
beamsolver install script

Install myfempy through `python setup.py install`,
or visit the github page to more information
"""
# SETUP SYSTEM
from setuptools import setup, find_packages

# README 
with open('README.md', 'r', encoding="utf-8") as ld:
    long_description = ld.read()

# VERSION
from beamsolver import version

# --------------
setup(
    python_requires=">=3",
    include_package_data=True,
    name="beamsolver",
    version=version.__version__,
    license="GNU",
    license_files=["LICENSE.txt"],
    author="Campos, A. V. G.",
    maintainer="Campos, A. V. G.",
    maintainer_email="antviniciuscampos@gmail.com",
    description="Symbolic Solver to Elastic Beam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avgcampos/BeamSolver",
    download_url="https://github.com/avgcampos/BeamSolver",
    keywords=["SoLids", "Mechanics", "Python Package", "Sympy"],
    packages=find_packages(),
    package_dir={
        "beamsolver": "beamsolver",
    },
    install_requires=[
        "sympy>=1.12"
        "numpy>=1.24",
        "matplotlib>=3.6",
        "art>=5.8",
        "colorama>=0.4",
    ],
    # include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOSX",
    ],
)
