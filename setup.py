#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing']

__import__('cmake')
from cmake import CMakeExtension, CMakeBuild

import os
from setuptools import setup, Extension

setup( name='stopeight',
       version='0.1.0',
       description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       license='GNU Lesser General Public License, version 2.1',
       url='http://www.stopeight.com',
       packages=_packages,
       ext_modules=[CMakeExtension('grapher',os.path.join('stopeight-clibs','grapher-wrappers'))],
       cmdclass=dict(build_ext=CMakeBuild),
       zip_safe=False,
)
