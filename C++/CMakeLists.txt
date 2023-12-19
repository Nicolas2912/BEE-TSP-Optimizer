cmake_minimum_required(VERSION 3.27)
project(CPP_Test)

set(CMAKE_CXX_STANDARD 23)

add_executable(CPP_Test
        TSP.cpp
        TSP.h
        Bee.cpp
        Bee.h
        main.cpp
)
