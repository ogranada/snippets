#!/usr/bin/python
# -*- coding: utf-8 -*-

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

