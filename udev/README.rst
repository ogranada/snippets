===============
 UDev snippets
===============

The snippets in this directory demonstrate libudev usage.


Available snippets
==================

Enumerate devices with udev
---------------------------

* ``udev_enumerate.py`` – Python with pyudev_
* ``udev_enumerate.cpp`` – C++ with libudev

These snippets illustrate the simplicity and readability of Python in contrast
to the almost insane complexity of C++, even for simple tasks.


Monitor devices with udev and Qt4
---------------------------------

Integrate a udev monitor into a Qt event loop to constantly monitor device
additions and removals.

* ``udev_monitor.py`` – Python with pyudev_ and PySide.
* ``udev_monitor.cpp`` – C++ with libudev and Qt4.

In these snippets the difference between the simplicity of Python and the
complexity of C++ is even more extreme than in the aforementioned snippets.


.. _pyudev: http://packages.python.org/pyudev
