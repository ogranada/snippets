cmake_minimum_required(VERSION 2.8)
project(snippets-designer-qt4)

set(QT_USE_IMPORTED_TARGETS ON)
find_package(Qt4 COMPONENTS QtCore QtGui)
if(QT4_FOUND)
  include(${QT_USE_FILE})
endif()

set(CMAKE_INCLUDE_CURRENT_DIR ON)

if(QT4_FOUND)
  message(STATUS "building qt4_static snippet")
  qt4_automoc(mainwindow.cpp)
  qt4_wrap_ui(qt4_static_uis mainwindow.ui)
  add_executable(qt4_static mainwindow.cpp qt4_static.cpp ${qt4_static_uis})
  set_target_properties(qt4_static PROPERTIES
    COMPILE_DEFINITIONS "QT_NO_CAST_FROM_ASCII;QT_NO_CAST_TO_ASCII")
  target_link_libraries(qt4_static ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY})
else()
  message(STATUS "skipping qt4_static snippet, Qt not found")
endif()
