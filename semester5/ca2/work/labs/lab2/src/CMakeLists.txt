cmake_minimum_required(VERSION 3.10)
project(calculator_project VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(calculator STATIC calculator.cpp)
target_include_directories(calculator PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(calc_app main.cpp)
target_link_libraries(calc_app PRIVATE calculator)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(calculator PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(calc_app PRIVATE -Wall -Wextra -Wpedantic)
endif()
