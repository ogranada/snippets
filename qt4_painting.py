#!/usr/bin/python
# Copyright (c) 2008, 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    qt4_painting
    ============

    Uses the Qt4 painting engine to paint a rotating spiral onto a widget.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import print_function

import sys
import math
from getopt import getopt

from PyQt4 import QtCore, QtGui, QtOpenGL


# allow to enable or disable the use of opengl
use_opengl = True
opts, args = getopt(sys.argv[1:], 'n', ['no-opengl'])
for opt, arg in opts:
    if opt in ('-n', '--no-opengl'):
        use_opengl = False


if use_opengl:
    # use QGLWidget as base class
    spiral_base = QtOpenGL.QGLWidget
    print('Enabling opengl support ...')
else:
    spiral_base = QtGui.QWidget
    print('Disabling opengl support ...')


class FunnySpiral(spiral_base):
    """
    Renders a spiral on a Qt widget.
    """

    def __init__(self, parent=None):
        super(spiral_base, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        # the timer, which drives the animation
        self.connect(self.timer, QtCore.SIGNAL('timeout()'),
                     self, QtCore.SLOT('update()'))
        # the angle, by which the spiral is rotated
        self.angle = 0
        self.spiral = self.update_spiral()

    def start_rotation(self):
        self.timer.start(100)

    def stop_rotation(self):
        self.timer.stop()

    def update_spiral(self):
        # create a polygon providing the corner points of the spiral
        polygon = QtGui.QPolygon()
        for i in xrange(self.window().width()):
            x = int(math.cos(i * 0.16) * i)
            y = int(math.sin(i * 0.16) * i)
            polygon.append(QtCore.QPoint(x, y))
        return polygon

    def resizeEvent(self, evt):
        # re-create the spiral, if the widget is resized
        self.spiral = self.update_spiral()

    def paintEvent(self, evt):
        # create a painter
        painter = QtGui.QPainter(self)
        # adjust the width of the pen
        pen = QtGui.QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        # enable high quality antialiasing
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        # move the center of the coordinate system to the widgets center
        painter.translate(self.width() / 2, self.height() / 2)
        # rotate the coordinate system by the given angle
        painter.rotate(self.angle)
        # draw the spiral
        painter.drawPolyline(self.spiral)
        # end painting and free resources
        painter.end()
        # update the angle
        self.angle += 30
        self.angle %= 360

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
