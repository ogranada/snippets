#!/usr/bin/python
# Copyright (c) 2008, 2009, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    Paint a rotating spiral in Qt.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
import math
from contextlib import contextmanager

from PySide.QtCore import QTimer, QPoint
from PySide.QtGui import (QApplication, QMainWindow, QPolygon, QPainter, QPen)
from PySide.QtOpenGL import QGLWidget


@contextmanager
def paint(paintdevice):
    painter = QPainter(paintdevice)
    yield painter
    painter.end()


class FunnySpiral(QGLWidget):
    """
    Renders a spiral on a Qt widget.
    """

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.timer = QTimer(self)
        # the timer, which drives the animation
        self.timer.timeout.connect(self.update)
        # the angle, by which the spiral is rotated
        self.angle = 0
        self.spiral = self.update_spiral()

    def start_rotation(self):
        self.timer.start(100)

    def stop_rotation(self):
        self.timer.stop()

    def update_spiral(self):
        # create a polygon providing the corner points of the spiral
        polygon = QPolygon()
        for i in xrange(self.window().width()):
            x = int(math.cos(i * 0.16) * i)
            y = int(math.sin(i * 0.16) * i)
            polygon.append(QPoint(x, y))
        return polygon

    def resizeEvent(self, evt):
        # re-create the spiral, if the widget is resized
        self.spiral = self.update_spiral()

    def paintEvent(self, evt):
        # create a painter
        with paint(self) as painter:
            # adjust the width of the pen
            pen = QPen()
            pen.setWidth(5)
            painter.setPen(pen)
            # enable high quality antialiasing
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
            # move the center of the coordinate system to the widgets center
            painter.translate(self.width() / 2, self.height() / 2)
            # rotate the coordinate system by the given angle
            painter.rotate(self.angle)
            # draw the spiral
            painter.drawPolyline(self.spiral)
            # end painting and free resources

        # update the angle
        self.angle += 30
        self.angle %= 360

class SpiralWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('A funny spiral')
        self.spiral = FunnySpiral(self)
        self.setCentralWidget(self.spiral)

    def closeEvent(self, event):
        self.spiral.stop_rotation()
        event.accept()

    def showEvent(self, event):
        self.spiral.start_rotation()

    def hideEvent(self, event):
        self.spiral.stop_rotation()


def main():
    app = QApplication(sys.argv)
    mainwindow = SpiralWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
