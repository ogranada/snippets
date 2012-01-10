==============================
 :dir:`udev` – UDev_ snippets
==============================

.. directory:: udev

The snippets in this directory demonstrate the usage of the Linux device
management libary udev_.  They are implemented in Python as well as C++, and
thus also serve as comparison between Python_ and C++.


Available snippets
==================

Device enumeration
------------------

Enumerate devices of specific type with libudev.

.. snippet:: udev_enumerate.py
   :synopsis: UDev device enumeration in Python

   Python with pyudev_

.. snippet:: udev_enumerate.cpp
   :synopsis: UDev device enumeration in C++

   C++ with libudev_.  This snippet uses safe udev pointers from :snippet:`udev_auto_ptr.hpp`.

These two snippets illustrate the simplicity and readability of Python in
contrast to the almost insane complexitly of C++, even for such simple tasks.


Monitor devices with udev and Qt4
---------------------------------

Integrate a udev monitor into a Qt event loop to constantly monitor device
additions and removals.

.. snippet:: udev_monitor.py
   :synopsis: UDev device monitoring in Python

   Python with pyudev_ and PySide_, using :py:class:`pyudev.Monitor` and
   :py:class:`pyudev.pyside.QUDevMonitorObserver`

.. snippet:: udev_monitor.h
             udev_monitor.cpp
   :synopsis: UDev device monitoring in C++

   C++ with Qt4_ and libudev_.  This snippet uses safe udev pointers from
   :snippet:`udev_auto_ptr.hpp` and the observer class from
   :snippet:`qudevobserver.h`.

In these snippets the difference between the simplicity of Python and the
complexity of C++ is even more extreme than in the aforementioned enumeration
snippets.


C++ helper files
----------------

These snippets support the implementation of the aforementioned C++ snippets.

.. snippet:: udev_auto_ptr.hpp
   :synopsis: Exception-safe UDev pointers for C++

   A standard C++ managed pointer atop of the libudev_ reference counting.
   This class allows to manage libudev_ resources in an exception-safe way.

.. snippet:: qudevobserver.h
             qudevobserver.cpp
   :synopsis: Turn UDev events into Qt signal

   Qt4_ class to observe a ``udev_monitor`` object from `libudev`_ and turn
   device events into Qt signals.

.. snippet:: CMakeLists.txt
   :synopsis: Build C++ with UDev

   Build the C++ snippets.


.. include:: references.rst
