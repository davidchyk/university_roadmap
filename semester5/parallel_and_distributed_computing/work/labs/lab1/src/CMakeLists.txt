cmake_minimum_required(VERSION 3.16)

project(lab1 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

find_package(Threads REQUIRED)

add_executable(lab1
    main.c
    include/data.c
)

target_include_directories(lab1 PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lab1 PRIVATE Threads::Threads)

if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(lab1 PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()
