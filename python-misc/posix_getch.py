# -*- coding: utf-8 -*-
# Copyright (c) 2012 Sebastian Wiesner <lunaryorn@googlemail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals, print_function

import sys
import os
import termios


def getch():
    """
    Read a keypress from the terminal and return the resulting character.

    The character is not echoed on the terminal. If a keypress is not already
    available this call will block.

    Return the character read from terminal as byte string.
    """
    tc_attrib = termios.tcgetattr(sys.stdin.fileno())
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = tc_attrib

    termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW,
                      [iflag, oflag, cflag,
                       lflag & ~termios.ICANON & ~termios.ECHO,
                       ispeed, ospeed, cc])

    try:
        return os.read(sys.stdin.fileno(), 1)
    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW,
                          [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])


def main():
    print('Enter a character:', end=' ')
    sys.stdout.flush()
    character = getch()
    print()
    print('Read character {0!r}'.format(character))


if __name__ == '__main__':
    main()
