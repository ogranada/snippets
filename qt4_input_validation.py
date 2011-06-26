#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

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

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtGui import (QMainWindow, QLineEdit, QDoubleValidator,
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
        # create a validator
        edit_validator = QDoubleValidator(self.edit)
        # and add it to the edito widget
        self.edit.setValidator(edit_validator)
        self.setCentralWidget(central)
        self.edit.returnPressed.connect(self.do_it)

    def do_it(self):
        QMessageBox.information(
            self, 'Do it!', 'The input was {0}'.format(self.edit.text()))
        number = float(self.edit.text())
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

