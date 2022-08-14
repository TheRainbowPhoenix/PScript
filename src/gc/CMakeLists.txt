cmake_minimum_required(VERSION 3.2)
project(MiniGC)

# set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

set(SOURCE_FILES
        gc.h
        gc.c
        )

add_library(gc SHARED STATIC ${SOURCE_FILES})  # remove "Static" for DLL
add_library(libgc SHARED ${SOURCE_FILES})
# TODO: manage DLL export ? + use lib in python for testing VM

set_target_properties(libgc PROPERTIES OUTPUT_NAME libgc)

# add these lines
include(GenerateExportHeader)
generate_export_header(gc)
generate_export_header(libgc)

install(TARGETS gc DESTINATION ${P_SCRIPT_INSTALL_INCLUDE_DIR})
install(TARGETS libgc DESTINATION ${P_SCRIPT_INSTALL_BIN_DIR})
# install(FILES gc.h DESTINATION ${P_SCRIPT_INSTALL_INCLUDE_DIR})