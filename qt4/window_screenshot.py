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
    Demonstrate how to take a screenshot of a QWidget.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Slot, QMetaObject
from PySide.QtGui import (QApplication, QMainWindow, QWidget, QLabel,
                          QPushButton, QVBoxLayout, QPixmap)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.image_label = QLabel('here\'s the shot', central)
        layout.addWidget(self.image_label)
        self.button = QPushButton('Shoot me!', central)
        self.button.setObjectName('shot_button')
        layout.addWidget(self.button)
        self.setCentralWidget(central)
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_shot_button_clicked(self):
        self.image_label.setPixmap(QPixmap.grabWidget(self))



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

