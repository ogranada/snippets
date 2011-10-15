===============
 Code snippets
===============

This site provides code snippets for various languages, libraries and
techniques.

The source code of the snippets is located in a :github:`GitHub repository
</>`.  This documentation is generated from commit |changeset| in this
repository.  Please :github:`report issues <issues>` or send :github:`pull
requests <pulls>`, if you've created a snippet you'd like to see in this
collection.


Available snippets
==================

.. toctree::
   :maxdepth: 1

   qt4/index
   python-misc
   udev
   misc


Qt4 snippets
------------

The largest part of this collection are :dir:`Qt4 snippets <qt4>`.  These
snippets show demonstrate modules and widgets from Qt4_, and show various
tricks and techniques to use in Qt4 applications.

These snippets are mainly Python_ snippets, with PySide_ used as binding, but
you'll find some PyQt4_ or even C++ snippets, too.


Miscellaneous Python_ snippets
------------------------------

Another large part of this collection consists of miscellaneous Python_
snippets in :dir:`python-misc`.  These snippets either demonstrate specific
Python modules, both standard library and 3rd party, but also some Python
tricks.


Usage instructions
==================

Most snippets can simply be executed with the corresponding interpreter.
Dependencies of snippets are not documented explicitly, but obvious in most, if
not all cases.  If in doubt simply inspect the source code and the build system
files and look for imports or includes.  The build system mostly notifies about
missing dependencies, in either case.


Python_ snippets
----------------

The collection contains snippets for both Python_ major versions.  As with
dependencies, the required interpreter version is not documented explicitly,
too.  Look at the source code to find out which interpreter to use.  The
presence of :py:mod:`__future__` imports typically indicates Python 2 snippets,
the lack thereof Python 3 snippets.  The shebang often also explicitly states
the major version to use.


C and C++ snippets
------------------

C and C++ snippets can be build with a standard CMake build system::

   mkdir build
   cd build
   cmake ..
   make

The build system shows status messages for each built snippet.  If dependencies
of a snippet are missing, the snippet is not build and a message with
information about the skipped snippet and its dependencies is shown.

Snippets in sub-directories have their own, isolated CMake build system.  Thus
you can build each subdirectory independently.  The following builds the udev
snippets only, for instance::

   cd udev
   mkdir build
   cd build
   cmake ..
   make

.. include:: references.rst
