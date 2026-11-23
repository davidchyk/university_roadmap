cmake_minimum_required(VERSION 3.20)
project(lab4_openmp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenMP REQUIRED)

add_executable(lab4 Lab4.cpp Data.cpp)
target_link_libraries(lab4 PRIVATE OpenMP::OpenMP_CXX)
target_compile_options(lab4 PRIVATE -O3 -Wall -Wextra -Wpedantic)
