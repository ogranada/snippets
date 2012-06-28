#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Sebastian Wiesner <lunaryorn@gmail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    onetimepad
    ==========

    A simple one-time-pad implementation for Python 3.

    Usage::

        # encryption
        $ python3 onetimepad.py keyfile myfile myfile.enc
        # decryption
        $ python3 onetimepad.py keyfile myfile.enc myfile

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""


import os
import sys
from operator import xor
from optparse import OptionParser


def main():
    parser = OptionParser(
        usage='%prog KEY [INPUT [OUTPUT]]',
        description='one-time-pad encryption')
    parser.add_option('-e', '--encrypt', action='store_false',
                      dest='decrypt',
                      help='Encrypt INPUT with KEY (default)')
    parser.add_option('-d', '--decrypt', action='store_true',
                      help='Decrypt INPUT using KEY')
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.error('missing key file')
    elif len(args) > 3:
        parser.error('superfluous arguments')

    keyfile = args[0]
    inputfile = args[1] if len(args) > 1 else '-'
    outputfile = args[2] if len(args) > 2 else '-'

    # read input data
    if inputfile == '-':
        data = sys.stdin.buffer.read()
    else:
        with open(inputfile, 'rb') as stream:
            data = stream.read()

    if opts.decrypt:
        # read and verify the key, if we are decrypting
        with open(keyfile, 'rb') as stream:
            key = stream.read()
        if len(key) < len(data):
            parser.error('invalid key in {}, {} keybytes missing'.format(
                keyfile, len(data) - len(key)))
    else:
        # generate and save the key, if we are encrypting
        key = os.urandom(len(data))
        with open(keyfile, 'wb') as stream:
            stream.write(key)

    # XOR data and key.  Encrypts or decrypts, depending on whether data is
    # plain text or cipher text
    result = bytes(map(xor, data, key))

    # write out the result of XOR
    if outputfile == '-':
        sys.stdout.buffer.write(result)
    else:
        with open(outputfile, 'wb') as stream:
            stream.write(result)


if __name__ == '__main__':
    main()
