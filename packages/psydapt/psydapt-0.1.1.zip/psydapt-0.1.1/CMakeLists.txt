cmake_minimum_required (VERSION 3.0)
set(CMAKE_CXX_STANDARD 17)
project(psydapt_py)

set(DEPS_DIR "${CMAKE_CURRENT_LIST_DIR}/submodules")

add_subdirectory("${DEPS_DIR}/psydapt")
add_subdirectory("${DEPS_DIR}/pybind11")
pybind11_add_module(psydapt_py src/main.cpp src/staircase.cpp src/questplus.cpp)

set_target_properties(psydapt_py PROPERTIES OUTPUT_NAME "psydapt")
target_link_libraries(psydapt_py PUBLIC psydapt)
