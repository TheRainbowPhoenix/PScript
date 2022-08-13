
cmake_minimum_required (VERSION 3.2)
project(PScript)

set(CMAKE_C_STANDARD 99)

set(P_SCRIPT_INSTALL_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(P_SCRIPT_INSTALL_BIN_DIR ${PROJECT_SOURCE_DIR}/bin)
set(P_SCRIPT_INSTALL_LIB_DIR ${PROJECT_SOURCE_DIR}/lib)

set(MINI_GC_HEADERS_DIR ${PROJECT_SOURCE_DIR}/src/gc)

include_directories(${P_SCRIPT_INSTALL_INCLUDE_DIR})
include_directories(${MINI_GC_HEADERS_DIR})

add_subdirectory(src)
add_subdirectory(test)


# add_executable(pgc main.c)