cmake_minimum_required (VERSION 3.2)

project(pscript)

add_subdirectory(gc)
set(SOURCE_FILES main.c)

add_executable(pscript ${SOURCE_FILES})
target_link_libraries(pscript gc)
install(TARGETS pscript DESTINATION ${P_SCRIPT_INSTALL_BIN_DIR})