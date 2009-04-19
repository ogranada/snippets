#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

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
    qt4_input_validation
    ====================

    Demonstrates the use of QValidator for input validation.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import (QMainWindow, QLineEdit, QDoubleValidator,
                         QMessageBox, QApplication, QWidget,
                         QVBoxLayout)


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Validation example')
        central = QWidget(self)
        central.setLayout(QVBoxLayout(central))
        self.edit = QLineEdit(central)
        central.layout().addWidget(self.edit)
        edit_validator = QDoubleValidator(self.edit)
        self.edit.setValidator(edit_validator)
        self.setCentralWidget(central)
        self.connect(self.edit, SIGNAL('returnPressed()'),
                     self.do_it)

    def do_it(self):
        QMessageBox.information(
            self, 'Do it!', 'The input was {0}'.format(self.edit.text()))
        number, ok = self.edit.text().toDouble()
        QMessageBox.information(
            self, 'Do it!', 'Convert to a double and add something: '
            '{0} + 2.5 = {1}'.format(number, number+2.5))


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

