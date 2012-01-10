====================================================
 :dir:`python-misc` – Miscellaneous Python snippets
====================================================

.. directory:: python-misc

This directory provides a unsorted collection of various Python snippets.  Some
of these demonstrate one or another Python programming technique, others show
how to use a specific library.


Available snippets
==================

.. snippet:: advanced_readline_usage.py
   :synopsis: readline usage

   :py:mod:`readline` fun

.. snippet:: conftool.py
   :synopsis: command line configuration editor

   A command-line configuration editor using configobj_

.. snippet:: du.py
   :synopsis: disk usage tool

   PoC `du(1)`_ implementation (somewhere from usenet)

.. snippet:: easy_uninstall.py
   :synopsis: PoC egg uninstallation

   PoC uninstall implementation for `easy\_install`_.

   .. warning::

      Don't even *think* of using this.  Use pip_ and distribute_!

.. snippet:: flatten_nested_lists.py
   :synopsis: Flatten nested lists

   Flattens nested lists

.. snippet:: magic_database.py
   :synopsis: mimetype and encoding detection with libmagic

   Detect mimetype and encoding of files using the Python binding of libmagic_

.. snippet:: onetimepad.py
   :synopsis: One-time pad cipher

   simple `one-time pad`_ implemented in Python 3

.. snippet:: ping.py
   :synopsis: ping implementation with raw sockets

   The classic `ping(8)`_ utility implemented in Python

.. snippet:: posix_getch.py
   :synopsis: POSIX getch() implementation

   POSIX-compatible implementation of :py:func:`msvcrt.getch()` with
   :py:mod:`termios`.  See :snippet:`/posix_getch.c` for a C implementation.

.. snippet:: pruefercode.py
   :synopsis: Prüfer code calculation

   Two different algorithms to calculate the Prüfer code for graphs

.. snippet:: pwgen.py
   :synopsis: random password generation

   Password generator implemented using :py:mod:`random`

.. snippet:: pycrypto_aes_padding.py
   :synopsis: AES with padding

   Enhances the AES_ implementation of pycrypto_ with proper padding

.. snippet:: screenshot.py
   :synopsis: Screenshots on X11

   Take screenshots by window title using `xwininfo(1)`_ and `import(1)`_ (from ImageMagick_)

.. snippet:: ssh_client.py
   :synopsis: SSH client with paramiko

   Simple paramiko_ demonstration

.. snippet:: xmpp_muc_logger.py
   :synopsis: Logging Jabber MUCs

   Log multiple Jabber MUCs using :py:mod:`threading` and xmpppy_

.. snippet:: xmpp_muc_logger_unthreaded.py
   :synopsis: Log a single Jabber MUC

   Log a single MUC, unthreaded


.. _configobj: http://www.voidspace.org.uk/python/configobj.html
.. _du(1): http://linux.die.net/man/1/du
.. _easy_install: http://packages.python.org/distribute/easy_install.html
.. _pip: http://pip-installer.org
.. _distribute: http://packages.python.org/distribute/index.html
.. _libmagic: http://www.darwinsys.com/file/
.. _one-time pad: http://en.wikipedia.org/wiki/One_Time_Pad
.. _ping(8): http://linux.die.net/man/8/ping
.. _AES: http://en.wikipedia.org/wiki/Advanced_Encryption_Standard
.. _pycrypto: https://www.dlitz.net/software/pycrypto/
.. _xwininfo(1): http://linux.die.net/man/1/xwininfo
.. _import(1): http://linux.die.net/man/1/import
.. _imagemagick: http://www.imagemagick.org/
.. _paramiko: http://www.lag.net/paramiko/
.. _xmpppy: http://xmpppy.sourceforge.net/
