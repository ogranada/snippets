# Copyright (c) 2010 Sebastian Wiesner <lunaryorn@gmail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    magic_database
    ==============

    Demonstrate the usage of the magic database in python.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
import os
import magic
from contextlib import closing


def guess_file_type(filename):
    """
    Guess the MIME-type and the encoding of ``filename`` (a string) using the
    magic database from libmagic.

    The MIME-type is almost alyways correct for binary files, and mostly
    (though not always) correct for text files.  The encoding is *guessed*,
    and may or may not be correct.  However, this guess is usually the best
    you can get.

    Return ``(mimetype, encoding)``.  Both tuple elements are strings.

    Raise :exc:`IOError`, if the magic database could not be loaded, and
    :exc:`OSError`, if an error occurred while accessing the given file.
    """
    with closing(magic.open(magic.MAGIC_MIME | magic.MAGIC_ERROR)) as db:
        if db.load() != 0:
            raise IOError('could not load magic database')
        result = db.file(filename)
        errno = db.errno()
        if errno != 0:
            raise OSError(errno, os.strerror(errno), filename)
        mimetype, encoding = result.split(';', 1)
        encoding = encoding.split('=', 1)[1]
        return mimetype, encoding


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit('missing filename')
    mimetype, encoding = guess_file_type(args[0])
    print('mimetype: {0}, encoding: {1}'.format(mimetype, encoding))


if __name__ == '__main__':
    main()
