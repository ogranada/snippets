===========================
 :dir:`qt4` – Qt4 snippets
===========================

.. directory:: qt4


Avialable snippets
==================

Designer usage
--------------

The subdirectory :dir:`qt4/designer` demonstrates how to use UI files created
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

  ``QFileSystemModel``-derived model, which adds checkboxes to file names

.. snippet:: countdown.py

  A simple PyQt4 countdown clock

.. snippet:: dbus_trayicon.py

  Combines Qt4 and python-dbus to create a remote-controllable,
  single-instance systray application

.. snippet:: foldable_checkboxes.py

  A special ``QTreeWidget``, which displays foldable groups of checkboxes.

.. snippet:: frameless_fullscreen.py

  Create a fullscreen window without frame

.. snippet:: painiting.py

  Paint a rotating spiral to demonstrate the Qt4 painting API

.. snippet:: icons_listview.py

  The art of having icons in your ``QListView``

.. snippet:: image_scaling.py

  A custom widget to draw and scale images

.. snippet:: input_validation.py

  Validating input using custom ``QValidator``\ s

.. snippet:: phonon_audio.py

  Using Phonon and PyQt4 to create a very simple audio player

.. snippet:: phonon_duplicate_video.py

  Duplicate video streams to different playback widgets using PyQt4 and
  Phonon (requires GStreamer backend)

.. snippet:: phonon_video.py

  Using Phonon and PyQt4 to create a very simple video player

.. snippet:: simple_shell_widget.py

  Live catching of subprocess output using ``QProcess``

.. snippet:: table_header_alignment.py

  Controlling the alignment of table headers ``QTableView``

.. snippet:: table_resize.py

  A simple ``QTableView``-derived class, which resizes columns
  automatically, if the view is resized

.. snippet:: tcp_socket.py

  Illustrates the use of Qt4's tcp network facilities by implementing a very
  simple chat program

.. snippet:: text_editor.py
             text_editor.ui

  A simple plain text editor.

.. snippet:: thread_progress.py

  A basic example for background threads and progress reporting with
  ``QProgressBar`` and ``QThread``

.. snippet:: toolbar_in_tabs.py

  Using toolbars within a ``QTabWidget`` with a bit of a dirty trick

.. snippet:: webkit_render_to_image.py

  render a website to an image file using PyQt4 and QtWebkit

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
