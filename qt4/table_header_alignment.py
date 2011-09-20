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
    Demonstrate how to align text in table headers with
    QTableView/QAbstractTableModel and QTableWidget.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Qt, QAbstractTableModel
from PySide.QtGui import (QMainWindow, QSplitter, QWidget, QLabel, QTableView,
                          QVBoxLayout, QTableWidget, QTableWidgetItem,
                          QApplication)


# The data displayed by the model
DATA = [
    # first row
    ['foo', 'bar'],
    # second row
    ['spam', 'eggs']
    ]


class TableModel(QAbstractTableModel):

    def rowCount(self, parent):
        # return the number of rows
        return len(DATA)

    def columnCount(self, parent):
        # return the number of columns
        return len(DATA[0])

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal:
            # don't use vertical headers!
            return
        if role == Qt.DisplayRole:
            # the text to display
            return 'No {0}'.format(section)
        elif role == Qt.TextAlignmentRole:
            # and the alignment
            return Qt.AlignRight
        else:
            return

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # the text to display!
            return DATA[index.row()][index.column()]
        elif role == Qt.TextAlignmentRole:
            # the alignment of the cell
            return Qt.AlignCenter
        else:
            return


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setup_ui()

    def setup_ui(self):
        splitter = QSplitter(self)
        left = QWidget(splitter)
        left.setLayout(QVBoxLayout(left))
        left.layout().addWidget(QLabel('QTableView', left))
        tableview = QTableView(left)
        tableview.setModel(TableModel(tableview))
        left.layout().addWidget(tableview)
        splitter.addWidget(left)
        right = QWidget(splitter)
        right.setLayout(QVBoxLayout(right))
        right.layout().addWidget(QLabel('QTableWidget', right))
        # create a table widget for DATA
        tablewidget = QTableWidget(len(DATA), len(DATA[1]), right)
        right.layout().addWidget(tablewidget)
        splitter.addWidget(right)
        self.setCentralWidget(splitter)

        # add tablewidget data
        self.add_data(tablewidget)

    def add_data(self, widget):
        # delete vertical headers
        for i in xrange(widget.rowCount()):
            widget.setVerticalHeaderItem(i, QTableWidgetItem())
        # set horizontal headers
        for i in xrange(widget.columnCount()):
            # the text
            item = QTableWidgetItem('No {0}'.format(i))
            # the alignment
            item.setTextAlignment(Qt.AlignRight)
            widget.setHorizontalHeaderItem(i, item)
        # set data
        for y, row in enumerate(DATA):
            for x, cell in enumerate(row):
                # the text
                item = QTableWidgetItem(cell)
                # the alignment
                item.setTextAlignment(Qt.AlignCenter)
                widget.setItem(y, x, item)


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
