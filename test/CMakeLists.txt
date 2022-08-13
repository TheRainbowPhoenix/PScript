cmake_minimum_required(VERSION 3.2)
project(pscript_tests)

# add_subdirectory(lib/googletest)

include_directories(${DIVISION_HEADERS_DIR})
# include_directories(lib/googletest/googletest/include)

set(SOURCE_FILES main.c src/pscript_tests.c)

add_executable(pscript_tests ${SOURCE_FILES})
target_link_libraries(pscript_tests gc) # gtest
install(TARGETS pscript_tests DESTINATION bin)