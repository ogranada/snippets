#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    A custom widget, which uses the Qt painting API to draw and scale images

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
from contextlib import contextmanager

from PySide.QtCore import Property, Qt, QDir
from PySide.QtGui import (QApplication, QWidget, QMainWindow, QPixmap, QImage,
                          QPainter, QIcon, QAction, QFileDialog)


@contextmanager
def paint(paintdevice):
    painter = QPainter(paintdevice)
    yield painter
    painter.end()


class ImageView(QWidget):
    def __init__(self, image=None, parent=None):
        QWidget.__init__(self, parent)
        self._image = None
        self._scale = False

    def _get_scale(self):
        return self._scale

    def _set_scale(self, value):
        if self._scale != value:
            self._scale = value
            self.update()

    def _get_image(self):
        return self._image

    def _set_image(self, image):
        self._image = image
        self.update()

    scale = Property(bool, _get_scale, _set_scale)
    image = Property(QImage, _get_image, _set_image)

    def paintEvent(self, event):
        if self._image is None:
            return QWidget.paintEvent(self, event)

        with paint(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
            pixmap = QPixmap.fromImage(self.image, Qt.AutoColor)
            scale_factor = 1.0
            if self._scale:
                scale_factor = min(self.width() / pixmap.width(),
                                   self.height() / pixmap.height())
            translated = (self.size() - (pixmap.size() * scale_factor)) / 2
            painter.translate(translated.width(), translated.height())
            painter.scale(scale_factor, scale_factor)
            painter.drawPixmap(0, 0, pixmap)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.image_viewer = ImageView(parent=self)
        self.setCentralWidget(self.image_viewer)

        exit = QAction(QIcon.fromTheme('application-exit'), 'Exit', self)
        open_image = QAction(QIcon.fromTheme('document-open'),
                             'Open image ...', self)
        scaling = QAction(QIcon.fromTheme('transform-scale'),
                          'Scale pixmap', self)
        scaling.setCheckable(True)

        actions = self.addToolBar('Actions')
        actions.addAction(exit)
        actions.addSeparator()
        actions.addAction(open_image)

        image_viewer_actions = self.addToolBar('Image viewer')
        image_viewer_actions.addAction(scaling)

        exit.triggered.connect(QApplication.instance().quit)
        open_image.triggered.connect(self._open_image)
        scaling.triggered[bool].connect(self._update_scaling)

    def _update_scaling(self, checked):
        self.image_viewer.scale = checked

    def _open_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open image ...', QDir.homePath(),
            "Images (*.tiff *.png *.xpm *.jpg)")
        if filename:
            self.image_viewer.image = QImage(filename)


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
