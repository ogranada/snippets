===============
 UDev snippets
===============

The snippets in this directory demonstrate libudev usage.


Available snippets
==================

``udev_auto_ptr.hpp``
  An auto pointer class for libudev types.  Wraps libudev reference counting
  semantics in an idiomatic C++ interface.

``udev_enumerate.cpp``
  Enumerate mouse devices with libudev.

``qudevobserver.h`` and ``qudevobserver.cpp``
  Emit signals for ``udev_monitor`` events.

``udev_monitor.h`` and ``udev_monitor.cpp``
  Monitor mouse devices with libudev and Qt.
