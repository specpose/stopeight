#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing']

import os
#cmake
#__import__('cmake')
#from cmake import CMakeExtension, CMakeBuild
#or distutils
__import__('monkey_patch_parallel')
__import__('python')
from python import get_pybind_include, BuildExt
my_path = os.path.dirname(os.path.realpath(__file__))

from setuptools import setup, Extension

setup( name='stopeight',
       version='0.1.0',
       description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       license='GNU Lesser General Public License, version 2.1',
       url='http://www.stopeight.com',
       packages=_packages,

#       ext_modules=[CMakeExtension('stopeight')],#,os.path.join('stopeight-clibs','grapher-wrappers'))],
#       cmdclass=dict(build_ext=CMakeBuild),
       ext_modules = [
           Extension(
               'stopeight.grapher',
               [os.path.join(my_path,'stopeight-clibs','grapher-wrappers','interfacepython.cpp')],
               include_dirs=[
                   # Path to pybind11 headers
                   get_pybind_include(),
                   get_pybind_include(user=True),
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','grapher')
               ],
               libraries=['stopeight-clibs-grapher'],
               language='c++'
           ),
           Extension(
               'stopeight.analyzer',
               [os.path.join(my_path,'stopeight-clibs','analyzer-wrappers','interfacepython.cpp')],
               include_dirs=[
                   os.path.join(my_path,'stopeight-clibs','analyzer/include')
               ],
               libraries=['stopeight-clibs-analyzer'],
               language='c++'
           ),
       ],
       install_requires=['pybind11>=2.2'],
       cmdclass={'build_ext': BuildExt},

       zip_safe=False,
)
