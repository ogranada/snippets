Snippets
========

.. contents::

C and C++ snippets
------------------

This section holds snippets written in C and C++ to demonstrate specific
techniques or implementation patterns

``posix_getch.c``
  POSIX compatible implementation of the ``getch()`` function from
  Microsoft C APIs


Python snippets
---------------

This section provides some general Python snippets as well as demonstrations
of some more specific APIs

``advanced_readline_usage.py``
  The powers of ``readline`` for completion and line editing

``conftool.py``
  A command-line configuration editor using configobj

``du.py``
  PoC ``du`` implementation (somewhere from usenet)

``easy_uninstall.py:``
  PoC uninstall implementation for ``easy_install``.  *Don't* use it in
  production, *don't* use ``easy_install`` in production:  There is ``pip``

``flatten_nested_lists.py``
  Flattens nested lists in python

``forking.py``
  Classic unix double fork for daemonizing

``magic_database.py``
  Detect mimetype and encoding of files using libmagic

``onetimepad.py``
  simple one-time-pad implemented in Python 3

``ping.py``
  The classic ``ping`` utility implemented in Python

``pruefercode.py``
  Two different algorithms to calculate the Prüfer code for graphs

``pwgen.py``
  Password generator implemented in python using the random module

``pycrypto_aes_padding.py``
  Enhances the AES implementation of pycrypto with proper padding

``screenshot.py``

  Take screenshots by window title using ``xwininfo`` and ``import`` (X11
  only)

``ssh_client.py``
  Simple paramiko demonstration

``xmpp_muc_logger.py``
  Log multiple Jabber MUCs using ``threading`` and ``xmpppy``

``xmpp_muc_logger_unthreaded.py``
  Log a single MUC, unthreaded


PyQt4
^^^^^

This section provides a wide variety of snippets for PyQt4, ranging from
model/view-programming to phonon multimedia art.

``qt4_checkable_filesystem_model.py``
  ``QFileSystemModel``-derived model, which adds checkboxes to file names

``qt4_configobj_editor.py``
  Combines Qt4, configobj and validate to create a generic config editor
  based on the configspec feature of configobj

``qt4-countdown.py``
  A simple PyQt4 countdown clock

``qt4_dbus_trayicon.py``
  Combines Qt4 and python-dbus to create a remote-controllable,
  single-instance systray application

``qt4_frameless_fullscreen.py``
  Create a fullscreen window without frame

``qt4_painiting.py``
  Paint a rotating spiral to demonstrate the Qt4 painting API

``qt4_icons_listview.py``
  The art of having icons in your ``QListView``

``qt4_input_validation.py``
  Validating input using custom ``QValidator``\ s

``qt4_phonon_audio.py``
  Using Phonon and PyQt4 to create a very simple audio player

``qt4_phonon_duplicate_video.py``
  Duplicate video streams to different playback widgets using PyQt4 and
  Phonon (requires GStreamer backend)

``qt4_phonon_video.py``
  Using Phonon and PyQt4 to create a very simple video player

``qt4_service_manager.py``
  A *very* simple service manager for ``/etc/init.d`` atop of ``QDirModel``

``qt4_simple_shell_widget.py``
  Live catching of subprocess output using ``QProcess``

``qt4_table_header_alignment.py``
  Controlling the alignment of table headers ``QTableView``

``qt4_table_resize.py``
  A simple ``QTableView``-derived class, which resizes columns
  automatically, if the view is resized

``qt4_tcp_socket.py``
  Illustrates the use of Qt4's tcp network facilities by implementing a very
  simple chat program

``qt4_thread_progress.py``
  A basic example for background threads and progress reporting with
  ``QProgressBar`` and ``QThread``

``qt4_toolbar_in_tabs.py``
  Using toolbars within a ``QTabWidget`` with a bit of a dirty trick

``qt4_webkit_render_to_image.py``
  render a website to an image file using PyQt4 and QtWebkit

``qt4_window_screenshot.py``
  Take a screenshot of the window client area and display the screenshot.

``qt4_xml_model.py``
  The power of custom model classes in Qt4


Other snippets
--------------

Miscellaneous snippets in various languages for various things

``kdialog_progressbar.bash``
  Demonstrate the progress bar mode of ``kdialog``


Comparing languages and libraries
---------------------------------

This section contains snippets, which compare implementations of a certain
technique or algorithm in different languages and different libraries


DBus signal handling in C, C++ and Python using Gtk and Qt4
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``dbus_glib_hal_signals.c``
  DBus signal handling using the dbus-glib bindings

``dbus_qt4_hal_signals.cpp``
  DBus signal handling using QtDBus

``dbus_glib_hal_signals.py``
  DBus signal handling using the python-dbus (shortest of course)


Usage instructions
------------------

The dependencies of the snippets are not explicitly documented.  Examine the
description and especially the source code of the snippets you are
interested in to find out, which dependencies must be installed for these
snippets.

If all dependencies are available, you can simply execute most snippets
using the corresponding interpreter.  However, C and C++ snippets need to be
compile first.  A cmake-based build system is provided for this task, just
run::

   mkdir build
   cd build
   cmake ..
   make

C and C++ snippets, whose dependencies are missing, are silently skipped.
If you are missing an executable for snippet, make sure, that really all
dependencies are installed.  Read the ``CMakeLists.txt``, if necessary.
