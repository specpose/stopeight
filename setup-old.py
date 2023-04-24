#!/usr/bin/env python

import os
_include_dirs=[
    os.path.join('stopeight-clibs','cmake-git-version-tracking','better-example'),
]
_qt5_include_dirs=_include_dirs
_library_dirs=[]

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_namespace_packages

setup( use_scm_version=True,
       packages=find_namespace_packages(include=['stopeight.*']),
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'pybind11',
           'setuptools_scm',
           ],
#pip start
       install_requires=[
          'numpy',
          'matplotlib',
          'PySide2',
          ],
#pip end
       ext_modules = [
           Pybind11Extension(
               'stopeight.grapher',
               [os.path.join('stopeight-clibs','grapher','python','IFPyGrapher.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','grapher')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-grapher',
               'stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Pybind11Extension(
               'stopeight.matrix',
               [os.path.join('stopeight-clibs','matrix','python','IFPyMatrix.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','matrix')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Pybind11Extension(
               'stopeight.analyzer',
               [os.path.join('stopeight-clibs','analyzer','python','IFPyAnalyzer.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','analyzer')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
#           Pybind11Extension(
#              'stopeight.legacy',
#               [os.path.join('stopeight-clibs','legacy','python','interfacepython.cpp'),
#               ],
#               include_dirs=_qt5_include_dirs + [
#                   os.path.join('stopeight-clibs','legacy/include'),
#                   os.path.join('stopeight-clibs','legacy','python')
#               ],
#               library_dirs=_library_dirs,
#               libraries=['stopeight-clibs-legacy','Qt5Core'],#Qt5Core needed for old wrapper
#               language='c++',
#               optional=True
#              ),
#            Pybind11Extension(
#              'stopeight.getters',
#               [os.path.join('stopeight-clibs','legacy','python','IFPyGetters.cpp'),
#               os.path.join('stopeight-clibs','legacy','python','IFPyShared.cpp')],
#               include_dirs=_qt5_include_dirs + [
#                   os.path.join('stopeight-clibs','legacy/include'),
#                   os.path.join('stopeight-clibs','legacy','python')
#               ],
#               library_dirs=_library_dirs,
#               libraries=['stopeight-clibs-legacy','stopeight-clibs-matrix','Qt5Core'],#Qt5Core needed for old wrapper
#               language='c++',
#               optional=True
#              ),
#            Pybind11Extension(
#              'stopeight.finders',
#               [os.path.join('stopeight-clibs','legacy','python','IFPyFinders.cpp'),
#               os.path.join('stopeight-clibs','legacy','python','IFPyShared.cpp')],
#               include_dirs=_qt5_include_dirs + [
#                   os.path.join('stopeight-clibs','legacy/include'),
#                   os.path.join('stopeight-clibs','legacy','python')
#               ],
#               library_dirs=_library_dirs,
#               libraries=['stopeight-clibs-legacy','stopeight-clibs-matrix','Qt5Core'],#Qt5Core needed for old wrapper
#               language='c++',
#               optional=True
#              ),
       ],
       cmdclass={'build_ext': build_ext},
)
