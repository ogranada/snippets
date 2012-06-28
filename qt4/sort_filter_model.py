#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Sebastian Wiesner <lunaryorn@gmail.com>

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
    sort_filter_model
    =================

    Sorting and filtering with ``QSortFilterProxyModel``.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Qt
from PySide.QtGui import (QApplication, QMainWindow, QWidget, QTableView,
                          QLineEdit, QVBoxLayout,
                          QSortFilterProxyModel, QStandardItemModel, QStandardItem)


class MainWindow(QMainWindow):

    COLUMNS = ['Name', 'Comment']

    ITEMS = [
        ('Ford', "Don't panic"),
        ('Marvin', "I'm feeling so depressed")
    ]

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi()
        # setup a sample model
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(self.COLUMNS)
        for row, item in enumerate(self.ITEMS):
            for column, cell in enumerate(item):
                self.model.setItem(row, column, QStandardItem(cell))
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        # filter all columns (use 0, 1, etc. to only filter by a specific column)
        self.proxy.setFilterKeyColumn(-1)
        # filter text case insensitively
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.view.setModel(self.proxy)
        for column, _ in enumerate(self.COLUMNS):
            self.view.resizeColumnToContents(column)
        self.searchBox.textChanged.connect(self.updateFilter)

    def updateFilter(self, text):
        self.proxy.setFilterFixedString(text)

    def setupUi(self):
        centralWidget = QWidget(self)
        centralWidget.setLayout(QVBoxLayout(centralWidget))
        self.view = QTableView(centralWidget)
        self.view.setSortingEnabled(True)
        centralWidget.layout().addWidget(self.view)
        self.searchBox = QLineEdit(centralWidget)
        centralWidget.layout().addWidget(self.searchBox)
        self.setCentralWidget(centralWidget)
        self.searchBox.setFocus()


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
