#!/usr/bin/python
# Copyright (c) 2008 Sebastian Wiesner <basti.wiesner@gmx.net>

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

from __future__ import print_function

import sys
import math
from getopt import getopt

from PyQt4 import QtCore, QtGui, QtOpenGL


use_opengl = True
opts, args = getopt(sys.argv[1:], 'n', ['no-opengl'])
for opt, arg in opts:
    if opt in ('-n', '--no-opengl'):
        use_opengl = False

if use_opengl:
    spiral_base = QtOpenGL.QGLWidget
    print('Enabling opengl support ...')
else:
    print('Enabling opengl support ...')
    spiral_base = QtGui.QWidget


class FunnySpiral(spiral_base):
    """
    Renders a spiral on a Qt widget.
    """

    def __init__(self, parent=None):
        spiral_base.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL('timeout()'),
                     self, QtCore.SLOT('update()'))
        self.angle = 0

    def start_rotation(self):
        self.timer.start(100)

    def stop_rotation(self):
        self.timer.stop()

    def paintEvent(self, evt):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        polygon = QtGui.QPolygon()
        for i in xrange(painter.window().width()):
            x = int(math.cos(i * 0.16) * i)
            y = int(math.sin(i * 0.16) * i)
            polygon.append(QtCore.QPoint(x, y))
        painter.drawPolyline(polygon)
        painter.end()
        self.angle += 30
        if self.angle >= 360:
            self.angle = self.angle - 360


class SpiralWindow(QtGui.QMainWindow):
    def __init__(self, use_opengl=True):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('A funny spiral')
        self.spiral = FunnySpiral(self)
        self.setCentralWidget(self.spiral)
        self.spiral.start_rotation()


def main():
    app = QtGui.QApplication(sys.argv)
    mainwindow = SpiralWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
