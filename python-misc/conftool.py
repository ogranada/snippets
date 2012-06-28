#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2007, 2008 Sebastian Wiesner <lunaryorn@gmail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
A simple script to edit INI-style configuration files from command line.
"""


import sys
import os
import locale
locale.setlocale(locale.LC_ALL, '')
from argparse import ArgumentParser

from configobj import ConfigObj, Section


def get(args):
    """Callback for ``get`` command. `args` ist the `argparse` namespace
    containing all command line options.
    """
    config = value = ConfigObj(args.file, file_error=True)
    for key in args.keys:
        value = value[key]
    if value is config:
        config.write(sys.stdout)
    elif isinstance(value, Section):
        ConfigObj(value).write(sys.stdout)
    else:
        print value


def set_(args):
    """Callback for ``set`` command. `args` is the `argparse` namespace
    containing all the command line options.
    """
    # descend to requested section. Create all intermediary sections if
    # necessary
    config = section = ConfigObj(args.file, create_empty=True)
    for name in args.sections:
        section = section.setdefault(name, {})
    section[args.option[0]] = args.value[0]
    config.write()


def delete(args):
    """Callback for ``del`` command. `args` is the `argparse` namespace
    containing all the command line options.
    """
    # walk down the line to the last specified key
    config = value = ConfigObj(args.file)
    for key in args.keys:
        section = value
        value = value[key]
    del section[key]
    if not args.keep_empty_sections:
        # remove the deleted key from the key list
        args.keys.pop()
        while section is not config:
            # walk up all sections and remove empty ones
            if section:
                break
            section = section.parent
            key = args.keys.pop()
            del section[key]
    if args.delete_file_if_empty and not config:
        # remove the file, if empty
        os.unlink(args.file)
    else:
        config.write()


def main():
    parser = ArgumentParser(
        description='Command line configuration reader and editor',
        epilog="""
Licensed under the terms of the WTFPL, version 2, as published by Sam
Dovecar. See http://sam.zoy.org/wtfpl/COPYING for details.""")
    parser.add_argument('-f', '--file', required=True,
                        help='The config file to work on.')
    subparsers = parser.add_subparsers()
    # get a config option
    get_parser = subparsers.add_parser('get', help='Get an option or '
                                       'section.')
    get_parser.add_argument('keys', nargs='*', metavar='key',
                            help='The key to get. This works '
                            'hierarchically. The last key is interpreted '
                            'as option name, any key before that evalutes '
                            'as section name. If no keys were given, the '
                            'whole file is printed (just like cat).')
    get_parser.set_defaults(callback=get)
    # set a config option
    set_parser = subparsers.add_parser('set', help='Set an option.')
    set_parser.add_argument('sections', nargs='*', metavar='section',
                            help='The sections, the option is stored in.')
    set_parser.add_argument('option', nargs=1, help='The option to set')
    set_parser.add_argument('value', nargs=1, help='The value')
    set_parser.set_defaults(callback=set_)
    # delete a config option
    del_parser = subparsers.add_parser('del', help='Delete an option or '
                                       'section.')
    del_parser.add_argument('keys', metavar='key', nargs='+',
                            help='Deletes, whatever the keys point to.')
    del_parser.add_argument('-k', '--keep-empty-sections',
                            help='If given, empty sections are not '
                            'deleted.', action='store_true')
    del_parser.add_argument('-d', '--delete-file-if-empty',
                            help='Deletes file, if is empty.',
                            action='store_true')
    del_parser.set_defaults(callback=delete)
    args = parser.parse_args()
    try:
        args.callback(args)
    except KeyError, err:
        parser.error('No such option or section: %s' % err)
    except IOError, err:
        parser.error(str(err))


if __name__ == '__main__':
    main()
