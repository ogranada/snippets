cmake_minimum_required(VERSION 2.8)
project(snippets)

message(STATUS "building posix_getch snippet")
add_executable(posix_getch posix_getch.c)

add_subdirectory(udev)
