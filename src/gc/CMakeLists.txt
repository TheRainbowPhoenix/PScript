cmake_minimum_required(VERSION 3.2)
project(MiniGC)

set(SOURCE_FILES
        gc.h
        gc.c
        )

add_library(gc SHARED STATIC ${SOURCE_FILES})  # remove "Static" for DLL
# TODO: manage DLL export ? + use lib in python for testing VM

install(TARGETS gc DESTINATION ${P_SCRIPT_INSTALL_LIB_DIR})
install(FILES gc.h DESTINATION ${P_SCRIPT_INSTALL_INCLUDE_DIR})