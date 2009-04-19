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
    qt4_window_screenshot
    =====================

    Demonstrates how to take a screenshot of a QWidget.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys
import subprocess

from PyQt4 import QtGui, QtCore


class MyMainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        central = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout(central)
        self.image_label = QtGui.QLabel('here\'s the shot', central)
        layout.addWidget(self.image_label)
        self.button = QtGui.QPushButton('Shoot me!', central)
        self.button.setObjectName('shot_button')
        layout.addWidget(self.button)
        self.setCentralWidget(central)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSignature('')
    def on_shot_button_clicked(self):
        # using import from ImageMagick
        # pass the window id to import, and read the image from standard
        # output
        ## proc = subprocess.Popen(
        ##     ['import', '-silent', '-window', str(self.winId()), 'png:-'],
        ##     stdout=subprocess.PIPE)
        ## stdout = proc.communicate()[0]
        ## image = QtGui.QImage()
        ## image.loadFromData(stdout)
        ## self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))

        # the right way!
        self.image_label.setPixmap(QtGui.QPixmap.grabWidget(self))



def main():
    app = QtGui.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

