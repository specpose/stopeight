#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

#print(version.__dict__['_version'])
from subprocess import check_output
import sys
#if sys.argv[1]=='sdist' or sys.argv[1]=='build' or sys.argv[1]=='install':
try:
    _version = check_output(['git', 'describe','--abbrev=0']).decode('utf-8').rstrip()
except:
    try:
        _version = check_output(['git', 'describe','--abbrev=0']).rstrip()
    except:
        _version = '0.0.0'
import os
_mod_version = 'HEAD'
try:
    _mod_version = check_output(['git','rev-parse','--short','HEAD']).decode('utf-8').rstrip()
except:
    _mod_version = check_output(['git','rev-parse','--short','HEAD']).rstrip()
_lib_version = 'HEAD'
try:
    _lib_version = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).decode('utf-8').rstrip()
except:
    _lib_version = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).rstrip()
file = open('version.py','w')
file.write('\"\"\"\n')
file.write("This file is auto-generated in setup.py\n")
file.write('\"\"\"\n')
file.write('_version = \''+str(_version)+'\'\n')
file.write('_mod_version = \''+str(_mod_version)+'\'\n')
file.write('_lib_version = \''+str(_lib_version)+'\'\n')
file.close()

import os
###cmake start
##__import__('cmake')
##from cmake import CMakeExtension, CMakeBuild
###cmake end
#distutils start
#__import__('monkey_patch_parallel')
__import__('python')
from python import get_pybind_include, BuildExt
my_path = os.path.dirname(os.path.realpath(__file__))
#distutils end

from setuptools import setup, Extension

setup( name='stopeight',
       version=_version,
       description='stopeight: Comparing sequences of points in 2 dimensions',
       long_description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       author_email='info@specpose.com',
       license='GNU General Public License, version 2',
       url='http://www.stopeight.com',
       python_requires='>=2.7',
       classifiers=[
           "Development Status :: 3 - Alpha",
           "Intended Audience :: Developers",
           "Topic :: Software Development :: Signal Analysis",
           "Topic :: Software Development :: Pen Stroke",
           "License :: OSI Approved :: GPL License",
           "Programming Language :: Python :: 2.7",
           "Programming Language :: Python :: 3",
           ],
       keywords="signal-analysis pen-stroke",
       packages=_packages,
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },

###cmake start
##       #ext_modules=[CMakeExtension('stopeight')],#,os.path.join('stopeight-clibs','grapher-wrappers'))],
##       ext_modules=[CMakeExtension('stopeight.analyzer'),CMakeExtension('stopeight.grapher'),CMakeExtension('stopeight.legacy')],
##       cmdclass=dict(build_ext=CMakeBuild),
###cmake end
#distutils start
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
           Extension(
              'stopeight.legacy',
               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','interfacepython.cpp')],
               include_dirs=[
                   os.path.join(my_path,'stopeight-clibs','legacy/include')
               ],
               libraries=['stopeight-clibs-legacy'],
               language='c++'
           ),
       ],
       cmdclass={'build_ext': BuildExt},
#pip start
       install_requires=[
          'numpy',
          'future',
          'funcsigs',
          'matplotlib',
          'pybind11>=2.2',#not for cmake
          'PyQt5>=5.6.0',
          ],
#pip end
#distutils end

       zip_safe=False,
)
