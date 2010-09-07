Snippets
========

- ``advanced_readline_usage.py``: demonstrates the usage of readline for
  completion and line editing
- ``CMakeLists.txt``: build instructions for all C and C++ sources
- ``conftool.py``: implements a command-line configuration editor using
  configobj
- ``dbus_glib_hal_signals.c``: demonstrates DBus signal handling using the
  dbus-glib bindings
- ``dbus_glib_hal_signals.py``: demonstrates DBus signal handling using the
  python-dbus (with glib as mainloop, which does however not really matter
  in this case)
- ``dbus_qt4_hal_signals.cpp``: demonstrates DBus signal handling using
  QtDBus
- ``du.py``: PoC ``du`` implementation (somewhere from usenet)
- ``easy_uninstall.py:``: PoC uninstall implementation for ``easy_install``
- ``flatten_nested_lists.py``:  flattens nested lists in python
- ``forking.py``: shows the classic unix double fork for daemonizing
- ``hal_touchpad_daemon.py``:  disables a synaptics touchpad, if mouse
  devices are plugged in.  The daemon listens on HAL to react on plugged
  mouse devices.
- ``kdialog_progressbar.bash``: demonstrates how to use the progress bar
  mode of ``kdialog``
- ``magic_database.py``: demonstrates how to use libmagic from python
- ``onetimepad.py``: simple one-time-pad for Python 3
- ``ping.py``: the classic ``ping`` utility implemented in Python
- ``posix_getch.c``: POSIX compatible implementation of the ``getch()``
  function from Microsofts C APIs
- ``pruefercode.py``: two different algorithms to calculate the Prüfer code
  for graphs
- ``pwgen.py``: password generator implemented in python using the random
  module
- ``pycrypto_aes_padding.py``: enhances the AES implementation of pycrypto
  with proper padding
- ``qt4_checkable_filesystem_model.py``: ``QFileSystemModel``-derived model,
  which adds checkboxes to file names
- ``qt4_configobj_editor.py``: combines Qt4, configobj and validate to
  create a generic config editor based on the configspec feature of
  configobj
- ``qt4-countdown.py``: a simple PyQt4 countdown app
- ``qt4_dbus_trayicon.py``: combines Qt4 and python-dbus to create a
  remote-controllable, single-instance systray application
- ``qt4_frameless_fullscreen.py``: shows how to create windows without
  frames and in fullscreen mode using PyQt4
- ``qt4_painiting.py``: demonstrates the use of the Qt4 painting API to
  paint a rotating spiral
- ``qt4_icons_listview.py``: how to display icons in a QListView
- ``qt4_input_validation.py``: how to use QValidator subclasses for input
  validation
- ``qt4_phonon_audio.py``: using Phonon and PyQt4 to create a very simple
  audio player
- ``qt4_phonon_duplicate_video.py``: duplicate video streams to different
  playback widgets using PyQt4 and Phonon (requires GStreamer backend for
  Phonon at point of writing)
- ``qt4_phonon_video.py``: using Phonon and PyQt4 to create a very simple
  video player
- ``qt4_service_manager.py``: uses ``QDirModel`` to create a simple service
  manager for ``/etc/init.d`` scripts
- ``qt4_simple_shell_widget.py``: demonstrates live catching of subprocess
  output using QProcess
- ``qt4_table_header_alignment.py``: how to align table headers in a
  QTableView
- ``qt4_table_resize.py``: a simple QTableView-derived class, which resizes
  columns automatically, if the view is resized
- ``qt4_tcp_socket.py``: illustrates the use of Qt4's tcp network
  facilities by implementing a very simple chat program
- ``qt4_thread_progress.py``: demonstrates how to report the progress of
  long-running background worker threads using QProgressBar and QThread
- ``qt4_toolbar_in_tabs.py``: how to use toolbars within a QTabWidget (using
  a bit of dirty trick)
- ``qt4_webkit_render_to_image.py``: render a website to an image file using
  PyQt4 and QtWebkit
- ``qt4_window_screenshot.py``: takes a screenshot of window client area and
  displays the screenshot
- ``qt4_xml_model.py``: demonstrates the powers of model classes in Qt4
- ``screenshot.py``: uses ``xwininfo`` and ``import`` to take screenshots
  based on window titles
- ``ssh_client.py``: demonstrates the use the paramiko API
- ``xmpp_muc_logger.py``: implements a logger for multiple Jabber MUCs
  using threading and xmpppy
- ``xmpp_muc_logger_unthreaded.py``: the same as above, but only for a
  single MUC, due to lack of threading

Use the following commands to build all C and C++ sources (make sure, that
all required libraries are installed!)::

   mkdir build
   cd build
   cmake ..
   make
