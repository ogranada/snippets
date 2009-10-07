cmake_minimum_required(VERSION 2.6)
project(snippets)

file(GLOB c_sources *.c)
foreach(c_source ${c_sources})
  get_filename_component(target ${c_source} NAME_WE)
  add_executable(${target} EXCLUDE_FROM_ALL ${c_source})
endforeach(c_source ${c_sources})

find_package(PkgConfig REQUIRED)
pkg_search_module(DBUS_GLIB REQUIRED dbus-glib-1)
include_directories(${DBUS_GLIB_INCLUDE_DIRS})
link_directories(${DBUS_GLIB_LIBRARY_DIRS})
target_link_libraries(dbus_glib_hal_signals ${DBUS_GLIB_LIBRARIES})
