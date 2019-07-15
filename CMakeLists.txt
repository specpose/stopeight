cmake_minimum_required(VERSION 3.1.3)

set(CMAKE_CXX_STANDARD 17)

project(stopeight)

add_subdirectory(pybind11)

#dont build clibs start
set(stopeight-clibs_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/stopeight-clibs/include
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)
#dont build clibs end

#build clibs start
#add_subdirectory(stopeight-clibs)
#build clibs end

#pybind11_add_module(grapher stopeight-clibs/grapher-wrappers/interfacepython.cpp)
#pybind11_add_module(analyzer stopeight-clibs/analyzer-wrappers/interfacepython.cpp)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory(stopeight-clibs/matrix-wrappers)
add_subdirectory(stopeight-clibs/grapher-wrappers)
add_subdirectory(stopeight-clibs/analyzer-wrappers)
add_subdirectory(stopeight-clibs/legacy-wrappers)
