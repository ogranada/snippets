# -*- coding: utf-8 -*-
# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


"""
    qt4_x11_key_names
    =================

    Shows how to get key names from key events on X11.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
from ctypes import CDLL, c_uint, c_char_p
from ctypes.util import find_library

from PyQt4.QtGui import QApplication, QWidget


libX11 = CDLL(find_library('X11'))
libX11.XKeysymToString.argtypes = [c_uint]
libX11.XKeysymToString.restype = c_char_p


class KeyNameWidget(QWidget):

    def show_event(self, name, event):
        keysym = event.nativeVirtualKey()
        keyname = libX11.XKeysymToString(keysym)
        print(name)
        print('    Qt keycode:', event.key())
        print('    Qt text:', unicode(event.text()))
        print('    X11 keysym:', keysym)
        print('    X11 keyname:', keyname)
        print()


    def keyPressEvent(self, event):
        self.show_event('KeyPressEvent', event)

    def keyReleaseEvent(self, event):
        self.show_event('KeyReleaseEvent', event)


def main():
    app = QApplication(sys.argv)
    widget = KeyNameWidget()
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()

