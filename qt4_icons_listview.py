#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009, 2010, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    qt4_icons_listview
    ==================

    How to show icons in a QListView.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import os
import sys

from PyQt4.QtCore import Qt, QSize, QAbstractListModel
from PyQt4.QtGui import QApplication, QMainWindow, QListView, QIcon


class IconModel(QAbstractListModel):
    def __init__(self, pages, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.pages = pages

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            name, icon = self.pages[index.row()]
            if role == Qt.DisplayRole:
                return name
            elif role == Qt.DecorationRole and icon:
                # return an icon, if the decoration role is used
                return icon
        return None

    def rowCount(self, index):
        return len(self.pages)


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    view = QListView(window)
    window.setCentralWidget(view)
    view.setViewMode(QListView.IconMode)
    view.setMovement(QListView.Static)
    view.setIconSize(QSize(64, 64))
    view.setModel(IconModel(
        [('System', QIcon.fromTheme('preferences-system')),
         ('Desktop', QIcon.fromTheme('preferences-desktop-personal'))],
        view))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

