cmake_minimum_required(VERSION 2.8.12)
project(stopeight)

add_subdirectory(pybind11)

set(stopeight-clibs_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/stopeight-clibs/include
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)

#pybind11_add_module(stopeight-clibs stopeight-clibs/grapher-wrappers/interfacepython.cpp)
add_subdirectory(stopeight-clibs/grapher-wrappers)
