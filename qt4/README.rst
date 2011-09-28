==============
 Qt4 snippets
==============

This directory contains an unsorted collection of snippets about Qt4.  Some
snippets demonstrate specific Qt classes or modules, some demonstrate general
Qt techniques, and some show more or less clever tricks.


Available snippets
==================

C++ snippets
------------

``qimage_from_gdk_pixbuf.cpp``
  Convert ``GdkPixbuf*`` to ``QImage``.


Python snippets
---------------

.. note::

   Most of these snippets are written with PySide, not PyQt4.


``checkable_filesystem_model.py``
  ``QFileSystemModel``-derived model, which adds checkboxes to file names

``countdown.py``
  A simple PyQt4 countdown clock

``dbus_trayicon.py``
  Combines Qt4 and python-dbus to create a remote-controllable,
  single-instance systray application

``foldable_checkboxes.py``
  A special ``QTreeWidget``, which displays foldable groups of checkboxes.

``frameless_fullscreen.py``
  Create a fullscreen window without frame

``painiting.py``
  Paint a rotating spiral to demonstrate the Qt4 painting API

``icons_listview.py``
  The art of having icons in your ``QListView``

``image_scaling.py``
  A custom widget to draw and scale images

``input_validation.py``
  Validating input using custom ``QValidator``\ s

``phonon_audio.py``
  Using Phonon and PyQt4 to create a very simple audio player

``phonon_duplicate_video.py``
  Duplicate video streams to different playback widgets using PyQt4 and
  Phonon (requires GStreamer backend)

``phonon_video.py``
  Using Phonon and PyQt4 to create a very simple video player

``simple_shell_widget.py``
  Live catching of subprocess output using ``QProcess``

``table_header_alignment.py``
  Controlling the alignment of table headers ``QTableView``

``table_resize.py``
  A simple ``QTableView``-derived class, which resizes columns
  automatically, if the view is resized

``tcp_socket.py``
  Illustrates the use of Qt4's tcp network facilities by implementing a very
  simple chat program

``text_editor.py`` and ``text_editor.ui``
  A simple plani text editor.

``thread_progress.py``
  A basic example for background threads and progress reporting with
  ``QProgressBar`` and ``QThread``

``toolbar_in_tabs.py``
  Using toolbars within a ``QTabWidget`` with a bit of a dirty trick

``webkit_render_to_image.py``
  render a website to an image file using PyQt4 and QtWebkit

``window_screenshot.py``
  Take a screenshot of the window client area and display the screenshot.

``x11_key_names.py``
  Turn key codes to X11 key names

``xml_model.py``
  The power of custom model classes in Qt4
