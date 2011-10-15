===========================
 :dir:`qt4` – Qt4 snippets
===========================

.. directory:: qt4


Avialable snippets
==================

Designer usage
--------------

The subdirectory :dir:`~qt4/designer` demonstrates how to use UI files created
with the Qt designer in C++ and Python.


C++ snippets
------------

.. snippet:: qimage_from_gdk_pixbuf.cpp

  Convert ``GdkPixbuf*`` to ``QImage``.


Python snippets
---------------

.. note::

   Most of these snippets are written with PySide, not PyQt4.


.. snippet:: checkable_filesystem_model.py

   :py:class:`~PySide.QtGui.QFileSystemModel`\ -derived model, which adds
   checkboxes to file names

.. snippet:: countdown.py

  A simple countdown clock

.. snippet:: dbus_trayicon.py

  Combines Qt4 and python-dbus to create a remote-controllable,
  single-instance systray application

.. snippet:: foldable_checkboxes.py

  A special :py:class:`~PySide.QtGui.QTreeWidget`, which displays foldable
  groups of checkboxes.

.. snippet:: frameless_fullscreen.py

  Create a fullscreen window without frame

.. snippet:: painiting.py

  Paint a rotating spiral to demonstrate the Qt4 painting API

.. snippet:: icons_listview.py

  The art of having icons in your :py:class:`~PySide.QtGui.QListView`

.. snippet:: image_scaling.py

  A custom widget to draw and scale images

.. snippet:: input_validation.py

  Validating input using a custom :py:class:`~PySide.QtGui.QValidator`

.. snippet:: phonon_audio.py

  Using :py:class:`~PySide.phonon.Phonon` to create a very simple audio player

.. snippet:: phonon_duplicate_video.py

  Duplicate video streams to different playback widgets using
  :py:mod:`~PySide.phonon.Phonon` (requires GStreamer backend)

.. snippet:: phonon_video.py

  Using :py:mod:`~PySide.phonon.Phonon` to create a very simple video player

.. snippet:: simple_shell_widget.py

  Live catching of subprocess output using :py:class:`~PySide.QtCore.QProcess`

.. snippet:: table_header_alignment.py

  Controlling the alignment of table headers
  :py:class:`~PySide.QtGui.QTableView`

.. snippet:: table_resize.py

  A simple :py:class:`~PySide.QtGui.QTableView`-derived class, which resizes
  columns automatically, if the view is resized

.. snippet:: tcp_socket.py

  Illustrates the use of Qt4's tcp network facilities by implementing a very
  simple chat program

.. snippet:: text_editor.py
             text_editor.ui

  A simple plain text editor.

.. snippet:: thread_progress.py

  A basic example for background threads and progress reporting with
  :py:class:`~PySide.QtGui.QProgressBar` and :py:class:`~PySide.QtCore.QThread`

.. snippet:: toolbar_in_tabs.py

  Using toolbars within a :py:class:`~PySide.QtGui.QTabWidget` with a bit of a
  dirty trick

.. snippet:: webkit_render_to_image.py

  render a website to an image file using :py:mod:`~PySide.QtWebkit`

.. snippet:: window_screenshot.py

  Take a screenshot of the window client area and display the screenshot.

.. snippet:: x11_key_names.py

  Turn key codes to X11 key names

.. snippet:: xml_model.py

  The power of custom model classes in Qt4


.. toctree::
   :hidden:

   designer


.. include:: ../references.rst
