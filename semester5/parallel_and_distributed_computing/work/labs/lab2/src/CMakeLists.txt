cmake_minimum_required(VERSION 3.16)

project(lab2 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

find_package(Threads REQUIRED)

add_executable(lab2
    main.c
    include/data.c
)

target_include_directories(lab2 PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lab2 PRIVATE Threads::Threads)

if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(lab2 PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()
