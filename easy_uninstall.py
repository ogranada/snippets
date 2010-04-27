#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2008, 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""
    easy_uninstall
    ==============

    Removes easy-installed packages.  Requires Python 2.6.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import print_function, division

__version__ = '0.2'

import os
import sys
import shutil
from optparse import OptionParser
from itertools import chain
from distutils import sysconfig

import pkg_resources


def error(msg, *args, **kwargs):
    """
    Print an error message to standard error.
    """
    print('ERROR:', msg.format(*args, **kwargs), file=sys.stderr)


def warn(msg, *args, **kwargs):
    """
    Print a warning message to standard error.
    """
    print('WARNING:', msg.format(*args, **kwargs), file=sys.stderr)


def info(msg, *args, **kwargs):
    """
    Print an information message to standard output.
    """
    print('**', msg.format(*args, **kwargs))


## file lookup

if not 'win32' in sys.platform:
    def find_scripts(distribution):
        """
        Find all scripts contained in the specified ``distribution``.
        """
        prefix = os.path.join(sys.exec_prefix, 'bin')
        script_names = chain(
            distribution.get_entry_map('gui_scripts').iterkeys(),
            distribution.get_entry_map('console_scripts').iterkeys())
        scripts = (os.path.join(prefix, s) for s in script_names)
        return (s for s in scripts if os.path.exists(s))

else:
    def find_scripts(distribution):
        """
        Find all scripts contained in the specified ``distribution``.
        """
        prefix = os.path.join(sys.exec_prefix, 'Scripts')
        ## TODO: finish implementation for windows
        warn('Scripts are not yet supported on windows')


def find_packages(distribution):
    """
    Find all python packages contained in the specified ``distribution``.
    """
    loc = distribution.location
    top_level = distribution.get_metadata_lines('top_level.txt')
    packages = (os.path.join(loc, p) for p in top_level)
    return (p for p in packages if os.path.exists(p))


def find_metadata(distribution):
    """
    Find all metadata files contained in the specified ``distribution``.
    """
    if os.path.exists(distribution.egg_info):
        yield distribution.egg_info

def remove_filenames(filenames, dry_run=False):
    """
    Remove all given files and directories.  If ``dry_run`` is ``True``,
    nothing is acutally done.
    """
    for name in filenames:
        if os.path.isdir(name):
            print('  << [dir]', name)
            dry_run or shutil.rmtree(
                name, onerror=lambda f, n, e: error('{0}', e[1]))
        else:
            print('  << [obj] ', name)
            try:
                dry_run or os.unlink(name)
            except EnvironmentError, err:
                error('{0}', err)


def cleanup_distribution_location(distribution, dry_run):
    """
    Remove the distribution location, if it's safe to remove, which
    basically means, that it is not the python library directory, and empty.
    """
    loc_path = os.path.normpath(distribution.location)
    if loc_path == os.path.normpath(sysconfig.get_python_lib()):
        return
    if os.path.isdir(loc_path) and os.listdir(loc_path):
        return
    remove_filenames([loc_path], dry_run)



def uninstall(name, dry_run=False):
    """Uninstalls the package denoted by ``name``."""
    try:
        info('Uninstalling {0}', name)
        distribution = pkg_resources.get_distribution(name)
        info('Removing scripts')
        remove_filenames(find_scripts(distribution), dry_run)
        info('Removing packages')
        remove_filenames(find_packages(distribution), dry_run)
        info('Removing metadata')
        remove_filenames(find_metadata(distribution), dry_run)
        info('Cleaning distribution location')
        cleanup_distribution_location(distribution, dry_run)
    except pkg_resources.DistributionNotFound:
        warn('Package {0} not found', name)


def main():
    parser = OptionParser(usage='%prog [-d] [package, ...]',
                          description='Removes easy_installed packages.',
                          epilog="""\
(C) 2008  Sebastian Wiesner, licensed under the terms of WTFPL 2.""")
    parser.add_option('-d', '--dry-run', action='store_true',
                      help="Don't actually do something")
    opts, args = parser.parse_args()
    if not args:
        parser.error('No packages specified')

    if opts.dry_run:
        info('Dry run, nothing is done')
    for arg in args:
        uninstall(arg, opts.dry_run)


if __name__ == '__main__':
    main()
