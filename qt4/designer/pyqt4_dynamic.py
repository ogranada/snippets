#!/usr/bin/python2
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
    How to load a user interface dynamically with PyQt4.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import os
import sys

from PyQt4.uic import loadUi
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QApplication, QMainWindow, QMessageBox


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # load the user interface dynamically into this object
        loadUi(os.path.join(SCRIPT_DIRECTORY, 'mainwindow.ui'), self)

    @pyqtSlot(bool)
    def on_clickMe_clicked(self, is_checked):
        if is_checked:
            message = self.trUtf8(b'I am checked now.')
        else:
            message = self.trUtf8(b'I am unchecked now.')
        QMessageBox.information(self, self.trUtf8(b'You clicked me'), message)

    @pyqtSlot()
    def on_actionHello_triggered(self):
        QMessageBox.information(self, self.trUtf8(b'Hello world'),
                                self.trUtf8(b'Greetings to the world.'))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
