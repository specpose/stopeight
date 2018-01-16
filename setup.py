#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

from subprocess import check_output
import sys
#if sys.argv[1]=='sdist' or sys.argv[1]=='build' or sys.argv[1]=='install':
try:
	_version = check_output(['git', 'describe','--abbrev=0']).decode('utf-8').rstrip()
except:
	try:
		_version = check_output(['git', 'describe','--abbrev=0']).rstrip()
#_version = '0.1.4'

import os
#cmake start
__import__('cmake')
from cmake import CMakeExtension, CMakeBuild
#cmake end
###distutils start
###__import__('monkey_patch_parallel')
##__import__('python')
##from python import get_pybind_include, BuildExt
##my_path = os.path.dirname(os.path.realpath(__file__))
###distutils end

from setuptools import setup, Extension

setup( name='stopeight',
       version=_version,
       description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       license='GNU General Public License, version 2',
       url='http://www.stopeight.com',
       packages=_packages,

#cmake start
       #ext_modules=[CMakeExtension('stopeight')],#,os.path.join('stopeight-clibs','grapher-wrappers'))],
       ext_modules=[CMakeExtension('stopeight.analyzer'),CMakeExtension('stopeight.grapher'),CMakeExtension('stopeight.legacy')],
       cmdclass=dict(build_ext=CMakeBuild),
#cmake end
###distutils start
##       ext_modules = [
##           Extension(
##               'stopeight.grapher',
##               [os.path.join(my_path,'stopeight-clibs','grapher-wrappers','interfacepython.cpp')],
##               include_dirs=[
##                   # Path to pybind11 headers
##                   get_pybind_include(),
##                   get_pybind_include(user=True),
##                   os.path.join(my_path,'stopeight-clibs','include'),
##                   os.path.join(my_path,'stopeight-clibs','grapher')
##               ],
##               libraries=['stopeight-clibs-grapher'],
##               language='c++'
##           ),
##           Extension(
##               'stopeight.analyzer',
##               [os.path.join(my_path,'stopeight-clibs','analyzer-wrappers','interfacepython.cpp')],
##               include_dirs=[
##                   os.path.join(my_path,'stopeight-clibs','analyzer/include')
##               ],
##               libraries=['stopeight-clibs-analyzer'],
##               language='c++'
##           ),
##           Extension(
##              'stopeight.legacy',
##               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','interfacepython.cpp')],
##               include_dirs=[
##                   os.path.join(my_path,'stopeight-clibs','legacy/include')
##               ],
##               libraries=['stopeight-clibs-legacy'],
##               language='c++'
##           ),
##       ],
##       cmdclass={'build_ext': BuildExt},
###pip start
##       install_requires=[
##          'numpy',
##          'future',
##          'funcsigs',
##          'matplotlib',
##          'pybind11>=2.2',#distutils
##          'PyQt5>=5.6.0',
##          ],
###pip end
###distutils end

       zip_safe=False,
)
