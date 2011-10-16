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

  :py:mod:`readline` fun

.. snippet:: conftool.py

  A command-line configuration editor using configobj_

.. snippet:: du.py

  PoC `du(1)`_ implementation (somewhere from usenet)

.. snippet:: easy_uninstall.py

  PoC uninstall implementation for `easy\_install`_.

  .. warning::

     Don't even *think* of using this.  Use pip_ and distribute_!

.. snippet:: flatten_nested_lists.py

  Flattens nested lists

.. snippet:: forking.py

  Classic unix double `fork(3)`_ for daemonizing

.. snippet:: magic_database.py

  Detect mimetype and encoding of files using the Python binding of libmagic_

.. snippet:: onetimepad.py

  simple `one-time pad`_ implemented in Python 3

.. snippet:: ping.py

  The classic `ping(8)`_ utility implemented in Python

.. snippet:: pruefercode.py

  Two different algorithms to calculate the Prüfer code for graphs

.. snippet:: pwgen.py

  Password generator implemented using :py:mod:`random`

.. snippet:: pycrypto_aes_padding.py

  Enhances the AES_ implementation of pycrypto_ with proper padding

.. snippet:: screenshot.py

  Take screenshots by window title using `xwininfo(1)`_ and `import(1)`_ (from ImageMagick_)

.. snippet:: ssh_client.py

  Simple paramiko_ demonstration

.. snippet:: xmpp_muc_logger.py

  Log multiple Jabber MUCs using :py:mod:`threading` and xmpppy_

.. snippet:: xmpp_muc_logger_unthreaded.py

  Log a single MUC, unthreaded


.. _configobj: http://www.voidspace.org.uk/python/configobj.html
.. _du(1): http://linux.die.net/man/1/du
.. _easy_install: http://packages.python.org/distribute/easy_install.html
.. _pip: http://pip-installer.org
.. _distribute: http://packages.python.org/distribute/index.html
.. _fork(3): http://linux.die.net/man/3/fork
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
