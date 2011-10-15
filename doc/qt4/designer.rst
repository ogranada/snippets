=============================================
 :dir:`qt4/designer` – Qt4 designer snippets
=============================================

.. directory:: qt4/designer


These snippets demonstrate how to use user interface created with the Qt
designer.

The sample userinterface is contained in :snippet:`mainwindow.ui`.


Python
======

The snippets :snippet:`pyqt4_dynamic.py` and :snippet:`pyside_dynamic.py`
demonstrate how to load user interfaces dynamically in PyQt4 and PySide
respectively.  Both snippets are written in Python 2.


.. snippet:: pyqt4_dynamic.py

   Dynamically load a user interface in PyQt4_.

.. snippet:: pyside_dynamic.py

   Dynamically load a user interface in PySide_.


C++
===

The snippet ``qt4_static.cpp``, together with ``mainwindow.h`` and
``mainwindow.cpp``, shows how to use a compiled user interface in C++.  The
user interface itself is compiled by ``uic``.  CMake provides a convenient
macro to invoke ``uic``, take a look at ``CMakeLists.txt``.


.. snippet:: mainwindow.h
             mainwindow.cpp
             qt4_static.cpp

   Compile and use a user interface in C++.


.. snippet:: CMakeLists.txt

   Build :snippet:`qt4_static.cpp`.


User interface file
===================

.. snippet:: mainwindow.ui

   The designer file used by the aforementioned snippets


.. include:: ../references.rst
