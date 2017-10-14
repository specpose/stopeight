cmake_minimum_required(VERSION 2.8.12)
project(stopeight)

add_subdirectory(pybind11)

set(stopeight-clibs_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/stopeight-clibs/include
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)
#add_subdirectory(stopeight-clibs)

#pybind11_add_module(grapher stopeight-clibs/grapher-wrappers/interfacepython.cpp)
#pybind11_add_module(analyzer stopeight-clibs/analyzer-wrappers/interfacepython.cpp)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory(stopeight-clibs/grapher-wrappers)
add_subdirectory(stopeight-clibs/analyzer-wrappers)
