cmake_minimum_required(VERSION 2.8)
project(snippets-qt4)

find_package(PkgConfig)
if(${PKG_CONFIG_FOUND})
  pkg_search_module(GDKPIXBUF gdk-pixbuf-2.0)
  if(${GDKPIXBUF_FOUND})
    include_directories(${GDKPIXBUF_INCLUDE_DIRS})
    link_directories(${GDKPIXBUF_LIBRARY_DIRS})
  endif(${GDKPIXBUF_FOUND})
endif(${PKG_CONFIG_FOUND})

set(QT_USE_IMPORTED_TARGETS ON)
find_package(Qt4 COMPONENTS QtCore QtGui)
if(${QT4_FOUND})
  include(${QT_USE_FILE})
endif(${QT4_FOUND})

if(${QT4_FOUND})
  if(${GDKPIXBUF_FOUND})
    message(STATUS "building qimage_from_gdk_pixbuf snippet")
    add_executable(qimage_from_gdk_pixbuf qimage_from_gdk_pixbuf.cpp)
    set_target_properties(qimage_from_gdk_pixbuf PROPERTIES
      COMPILE_DEFINITIONS "QT_NO_CAST_FROM_ASCII;QT_NO_CAST_TO_ASCII")
    target_link_libraries(qimage_from_gdk_pixbuf QtCore QtGui
      ${GDKPIXBUF_LIBRARIES})
  endif(${GDKPIXBUF_FOUND})
endif(${QT4_FOUND})
