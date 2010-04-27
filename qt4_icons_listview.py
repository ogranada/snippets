#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

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

from PyQt4 import QtCore, QtGui


class Model(QtCore.QAbstractListModel):
    def __init__(self, pages, parent=None):
        super(QtCore.QAbstractListModel, self).__init__(parent)
        self.pages = pages

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            name, icon = self.pages[index.row()]
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(name)
            elif role == QtCore.Qt.DecorationRole and icon:
                # return an icon, if the decoration role is used
                return QtCore.QVariant(icon)
        return QtCore.QVariant()

    def rowCount(self, index):
        return len(self.pages)



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setup_ui()

    def find_icon(self, name):
        path = os.path.join(
            '/usr/share/icons/oxygen/scalable/categories', name + '.svgz')
        if os.path.isfile(path):
            return QtGui.QIcon(path)
        else:
            return None

    def setup_ui(self):
        view = QtGui.QListView(self)
        view.setViewMode(QtGui.QListView.IconMode)
        view.setMovement(QtGui.QListView.Static)
        view.setIconSize(QtCore.QSize(64, 64))
        pages = [
            ('System', self.find_icon('preferences-system')),
            ('Desktop', self.find_icon('preferences-desktop-personal'))]
        model = Model(pages, self)
        view.setModel(model)
        self.setCentralWidget(view)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

