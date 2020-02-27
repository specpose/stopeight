#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

import os
#distutils start
#__import__('monkey_patch_parallel')
__import__('python')
from python import get_pybind_include, BuildExt
my_path = os.path.dirname(os.path.realpath(__file__))
from distutils import sysconfig
_include_dirs=[
    os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example'),
    # Path to pybind11 headers
    get_pybind_include(),
    get_pybind_include(user=True),
]
_qt5_include_dirs=_include_dirs
if sysconfig.get_path('include')!='None':
    _qt5_include_dirs.append(os.path.join(str(sysconfig.get_path('include')),'qt5')) #ubuntu only
    _qt5_include_dirs.append(os.path.join(str(sysconfig.get_path('include'))))
#distutils end

from setuptools import setup, Extension

setup( use_scm_version=True,
       packages=_packages,
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'pybind11>=2.4',
           'setuptools_scm',
           ],
       zip_safe=False,
#distutils start
#pip start
       install_requires=[
          'numpy<1.17.0',#python2
          'future',
          'funcsigs',
          'matplotlib<3.0',#python2
          'pybind11>=2.4',
          'PyQt5<5.11.0',# <5.11.0, because pip>=19.3 #not for python2
          ],
#pip end
       ext_modules = [
           Extension(
               'stopeight.grapher',
               [os.path.join(my_path,'stopeight-clibs','grapher-wrappers','IFPyGrapher.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','grapher')
               ],
               libraries=['stopeight-clibs-grapher'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.matrix',
               [os.path.join(my_path,'stopeight-clibs','matrix-wrappers','IFPyMatrix.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','matrix')
               ],
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.analyzer',
               [os.path.join(my_path,'stopeight-clibs','analyzer-wrappers','IFPyAnalyzer.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','analyzer')
               ],
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
           Extension(
              'stopeight.legacy',
               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','interfacepython.cpp')],
               include_dirs=_qt5_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','legacy/include')
               ],
               libraries=['stopeight-clibs-legacy'],
               language='c++',
               optional=True
              ),
       ],
       cmdclass={'build_ext': BuildExt},
#distutils end
)
