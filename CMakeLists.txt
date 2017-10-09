cmake_minimum_required(VERSION 2.8.12)
project(grapher)

add_subdirectory(pybind11)
pybind11_add_module(grapher stopeight-clibs/grapher-wrappers/interfacepython.cpp)
