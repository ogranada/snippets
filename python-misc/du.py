#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

import os
import sys
import math
from itertools import chain, ifilterfalse, imap


__all__ = ['format_bytesize', 'dir_and_filenames', 'dir_statistic',
           'print_sizes']


# (Short) Names for 1024 based data size units:  Bytes, KibiBytes,
# MebiBytes, ...
#
# TODO: Note down reference to ISO/IEC standard here.
UNIT_NAMES = ('B', 'KiB', 'MiB', 'GiB', 'TiB')


def format_bytesize(size, precision=1):
    """Fomats a `size` in bytes as string with a unit attached.

    The unit is one of 'B', 'KiB', 'MiB', 'GiB', and 'TiB'.  The number is
    formatted so that it has the smallest possible unit but not more than 3
    digits before the decimal point.  Unless it's more then 999 terabytes
    of course.

    How many digits are placed after the decimal point depends on the
    `precision` parameter.  If the `size` can be formatted as bytes there's
    no fractional part at all.

    :raises ValueError: if `size` is negative.
    """
    if size < 0:
        raise ValueError('negative size (%r)' % size)

    # As long as there are more than 3 digits in the integer part of the size
    # and there is a higher unit, divide `size` by 1024.
    power = 0
    while size and math.log10(size) >= 3 and power < len(UNIT_NAMES):
        power += 1
        size /= 1024

    # A size given in bytes does not have a fractional part.
    if power == 0:
        number_format = '%d'
    else:
        number_format = '%%.%df' % precision

    return (number_format + ' %-3s') % (size, UNIT_NAMES[power])


def dir_and_filenames(path):
    """Collects all directory names and file names plus file sizes found at
    given `path` (non-recursive).

    Both sequences are sorted by name.

    Symbolic links are ignored to prevent special cases like dead links.

    :returns: a tuple of directory names and file names plus file sizes.
    :rtype: ([str], [(str, int)])
    """
    dirnames = []
    filenames_and_sizes = []
    for name in os.listdir(path):
        fullname = os.path.join(path, name)
        if not os.path.islink(fullname):
            if os.path.isdir(fullname):
                dirnames.append(name)
            elif os.path.isfile(fullname):
                filenames_and_sizes.append((name, os.path.getsize(fullname)))
    dirnames.sort()
    filenames_and_sizes.sort()
    return (dirnames, filenames_and_sizes)


def dir_statistic(path):
    """Counts all files, subdirectories and their total size untder given
    `path` recursivly.

    Symbolic links to files and directories are ignored.

    :returns: a tuple with directory count, file count and total size.
    :rtype: (int, int, int)
    """
    dir_count = 0
    file_count = 0
    total_size = 0
    for pathname, dirnames, filenames in os.walk(path):
        dir_count += len(dirnames)
        file_count += len(filenames)
        fullnames = (os.path.join(pathname, x) for x in
                     chain(dirnames, filenames))
        total_size += sum(imap(os.path.getsize,
                               ifilterfalse(os.path.islink, fullnames)))
    return (dir_count, file_count, total_size)


def print_sizes(path):
    """Prints the sizes and names of the directories under `path` (recursivly)
    and the sizes and names of the files under `path` (non-recursive) plus a
    grand total of bytes.
    """
    grand_total = 0
    (dirnames, filenames_and_sizes) = dir_and_filenames(path)
    print '    size       type   dirs/files name'
    print ':' * 70

    # Print directories.
    for dirname in dirnames:
        fullname = os.path.join(path, dirname)
        (dir_count, file_count, total_size) = dir_statistic(fullname)
        grand_total += total_size
        print '%12s   DIR   %5d/%-5d %s' % (format_bytesize(total_size),
                                            dir_count, file_count, dirname)

    # Print files.
    for (name, size) in filenames_and_sizes:
        grand_total += size
        print '%12s   file              %s' % (format_bytesize(size), name)

    # And the grand total.
    print '------------------\n%12s total' % format_bytesize(grand_total)


if __name__ == '__main__':
    print_sizes(sys.argv[1])
