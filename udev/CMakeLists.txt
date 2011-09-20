cmake_minimum_required(VERSION 2.8)
project(snippets-udev)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

find_package(PkgConfig)
if(${PKG_CONFIG_FOUND})
  pkg_search_module(LIBUDEV libudev)
  if(${LIBUDEV_FOUND})
    include_directories(${LIBUDEV_INCLUDE_DIRS})
    link_directories(${LIBUDEV_LIBRARY_DIRS})
  endif(${LIBUDEV_FOUND})
endif(${PKG_CONFIG_FOUND})

set(QT_USE_IMPORTED_TARGETS ON)
find_package(Qt4 COMPONENTS QtCore)
if(${QT4_FOUND})
  include(${QT_USE_FILE})
endif(${QT4_FOUND})

set(qt_no_ascii_definitions QT_NO_CAST_FROM_ASCII QT_NO_CAST_TO_ASCII)

if(${LIBUDEV_FOUND})
  message(STATUS "building udev_enumerate snippet")
  add_executable(udev_enumerate udev_auto_ptr.hpp udev_enumerate.cpp)
  target_link_libraries(udev_enumerate ${LIBUDEV_LIBRARIES})
  # set_target_properties(udev_enumerate PROPERTIES
  #   COMPILE_DEFINITIONS ${qt_no_ascii_definitions})
  if(${QT4_FOUND})
    message(STATUS "building udev_monitor snippet")
    set(udev_monitor_sources qudevobserver.cpp udev_monitor.cpp)
    set(udev_monitor_headers udev_auto_ptr.hpp qudevobserver.h udev_monitor.h)
    qt4_automoc(${udev_monitor_sources})
    add_executable(udev_monitor ${udev_monitor_sources} ${udev_monitor_headers})
    target_link_libraries(udev_monitor QtCore ${LIBUDEV_LIBRARIES})
    # set_target_properties(udev_monitor PROPERTIES
    #   COMPILE_DEFINITIONS ${qt_no_ascii_definitions})
  else(${QT4_FOUND})
    message(STATUS "skipping udev_monitor snippet, QtCore not found")
  endif(${QT4_FOUND})
else(${LIBUDEV_FOUND})
  message(STATUS
    "skipping udev_enumerate and udev_monitor snippets, libudev not found")
endif(${LIBUDEV_FOUND})



