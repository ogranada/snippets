==================
 Designer support
==================

These snippets demonstrate how to use user interface created with the Qt
designer.

The sample userinterface is contained in ``mainwindow.ui``.


Python
======

The snippets ``pyqt4_dynamic.py`` and ``pyside_dynamic.py`` demonstrate how to
load user interfaces dynamically in PyQt4 and PySide respectively.  Both
snippets are written in Python 2.


C++
===

The snippet ``qt4_static.cpp``, together with ``mainwindow.h`` and
``mainwindow.cpp``, shows how to use a compiled user interface in C++.  The
user interface itself is compiled by ``uic``.  CMake provides a convenient
macro to invoke ``uic``, take a look at ``CMakeLists.txt``.
