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
    qt4_webkit_render_to_image
    ==========================

    Renders a website to an image.  Usage:

        render_image.py http://example.com /path/to/image.png

    Requires PyQt 4.5 and Python 2.6.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import QObject, QUrl
from PySide.QtGui import QApplication, QImage, QPainter
from PySide.QtWebKit import QWebPage


class ImageRenderer(QObject):

    def __init__(self, url, image_path):
        QObject.__init__(self)
        self.url = QUrl(url)
        self.image_path = image_path
        self.webpage = QWebPage(self)
        self.webpage.loadFinished.connect(self.render)
        self.webpage.mainFrame().load(self.url)

    def render(self, ok):
        if ok:
            print('Loaded {0}'.format(self.url.toString()))
            self.webpage.setViewportSize(
                self.webpage.mainFrame().contentsSize())
            image = QImage(self.webpage.viewportSize(),
                           QImage.Format_ARGB32)
            painter = QPainter(image)

            self.webpage.mainFrame().render(painter)
            painter.end()

            if image.save(self.image_path):
                print('Saved image to {0}'.format(self.image_path))
            else:
                print('Could not save to {0}'.format(self.image_path))
        else:
            print('Could not load {0.toString()}'.format(self.url))

        QApplication.instance().quit()


def main():
    if len(sys.argv) < 3:
        sys.exit('please specifiy website url and image path')
    website, image_path = sys.argv[1], sys.argv[2]
    app = QApplication(sys.argv)
    renderer = ImageRenderer(website, image_path)
    app.exec_()


if __name__ == '__main__':
    main()
