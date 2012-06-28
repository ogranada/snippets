#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009, 2011 Sebastian Wiesner <lunaryorn@gmail.com>

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
    How to create a frameless toplevel widget without visible mouse cursor.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QMainWindow, QMenu, QAction


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # activate the window and use the full screen
        self.setWindowState(Qt.WindowFullScreen | Qt.WindowActive)
        # empty the mouse cursor
        self.setCursor(Qt.BlankCursor)
        # add a menu to close the window
        appmenu = QMenu('&Application', self)
        quit = QAction('&Quit', self)
        appmenu.addAction(quit)
        self.menuBar().addMenu(appmenu)
        quit.triggered.connect(QApplication.instance().quit)


def main():
    app = QApplication(sys.argv)
    mywindow = MyMainWindow()
    mywindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
