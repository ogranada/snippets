#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    pwgen
    =====

    Demonstrates usage of the random module to generate passwords.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import os
import sys
import string
from random import SystemRandom
random = SystemRandom()


def generate_password(length, letters=string.ascii_letters):
    """
    Generates a password from ``letters`` (defaults to
    `string.ascii_letters`).

    :param length:  Length of the password
    :type length: int
    :param letters:  letters to be used in the password
    :type letters:  sequence
    :return:  The generated password
    :returntype: str
    """
    return ''.join(random.choice(letters) for i in xrange(length))


def main():
    progname = os.path.basename(sys.argv[0])
    args = sys.argv[1:]
    if not args:
        print >> sys.stderr, 'Usage: %s length' % progname
        return
    try:
        length = int(args[0])
    except ValueError:
        print >> sys.stderr, 'error:%s: length must be a number' % progname
    else:
        print generate_password(length)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Abgebrochen'

