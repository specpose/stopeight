#!/usr/bin/env python

import os
#cmake start
__import__('cmake')
from cmake import CMakeExtension, CMakeBuild
#cmake end

from setuptools import setup, Extension, find_namespace_packages

setup( use_scm_version=True,
       packages=find_namespace_packages(include=['stopeight.*']),
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools_scm',
           ],
#pip start - not in cmake_examples
       install_requires=[
          'numpy',
          'matplotlib',
          'PySide2',
          ],
#pip end - not in cmake_examples
#cmake start
#Hack for faster compile. --inplace and copy_extensions_to_source to working anyway
#       ext_modules=[CMakeExtension('stopeight.matrix',''),CMakeExtension('stopeight.grapher',''),CMakeExtension('stopeight.analyzer',''),CMakeExtension('stopeight.legacy','')],
       ext_modules=[CMakeExtension('stopeight.stopeight-clibs','')],
       cmdclass=dict(build_ext=CMakeBuild),
#cmake end
)
