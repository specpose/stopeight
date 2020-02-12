#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

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
from distutils import sysconfig
#distutils end

from setuptools import setup, Extension

setup( name='stopeight',
       version_format='{tag}.dev{commitcount}+{gitsha}',
       description='stopeight: Comparing sequences of points in 2 dimensions',
       long_description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       author_email='fassio@specpose.com',
       license='GNU General Public License, version 2',
       url='https://github.com/specpose/stopeight',
       python_requires='>=2.7',
       classifiers=[
           "Development Status :: 3 - Alpha",
           "Intended Audience :: Developers",
           "Topic :: Multimedia :: Sound/Audio :: Analysis",
           "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
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
##       ext_modules=[CMakeExtension('stopeight.matrix'),CMakeExtension('stopeight.analyzer'),CMakeExtension('stopeight.grapher'),CMakeExtension('stopeight.legacy')],
##       cmdclass=dict(build_ext=CMakeBuild),
###cmake end
#distutils start
       ext_modules = [
           Extension(
               'stopeight.grapher',
               [os.path.join(my_path,'stopeight-clibs','grapher-wrappers','IFPyGrapher.cpp')],
               include_dirs=[
                   # Path to pybind11 headers
                   get_pybind_include(),
                   get_pybind_include(user=True),
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','grapher'),
		   os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example')
               ],
               libraries=['stopeight-clibs-grapher'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.matrix',
               [os.path.join(my_path,'stopeight-clibs','matrix-wrappers','IFPyMatrix.cpp')],
               include_dirs=[
                   # Path to pybind11 headers
                   get_pybind_include(),
                   get_pybind_include(user=True),
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','matrix'),
		   os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example')
               ],
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.analyzer',
               [os.path.join(my_path,'stopeight-clibs','analyzer-wrappers','IFPyAnalyzer.cpp')],
               include_dirs=[
                   # Path to pybind11 headers
                   get_pybind_include(),
                   get_pybind_include(user=True),
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','analyzer'),
		   os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example')
               ],
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
           Extension(
              'stopeight.legacy',
               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','interfacepython.cpp')],
               include_dirs=[
                   os.path.join(my_path,'stopeight-clibs','legacy/include'),
		   os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example'),
                   os.path.join(str(sysconfig.get_config_var('INCLUDEDIR')),str(sysconfig.get_config_var('MULTIARCH')),'qt5')#ubuntu only
               ],
               libraries=['stopeight-clibs-legacy'],
               language='c++',
               optional=True
              ),
       ],
       cmdclass={'build_ext': BuildExt},
#pip start
       install_requires=[
          'numpy',
          'future',
          'funcsigs',
          'matplotlib',
          'pybind11>=2.3',#not for cmake
          'PyQt5<5.11.0',# <5.11.0, because pip>=19.3 #also >=5.6.0 pip2 doesn't support it!
          ],
#pip end
#distutils end
       setup_requires=[
           'setuptools-git-version',
           ],
       zip_safe=False,
)
