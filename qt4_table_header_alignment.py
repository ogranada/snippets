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
    qt4_table_header_alignment
    ==========================

    Demonstrates how to align text in table headers with
    QTableView/QAbstractTableModel and QTableWidget.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import sys

from PyQt4 import QtCore, QtGui


# The data displayed by the model
DATA = [
    # first row
    ['foo', 'bar'],
    # second row
    ['spam', 'eggs']
    ]


class TableModel(QtCore.QAbstractTableModel):

    def rowCount(self, parent):
        # return the number of rows
        return len(DATA)

    def columnCount(self, parent):
        # return the number of columns
        return len(DATA[0])

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Horizontal:
            # don't use vertical headers!
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            # the text to display
            return QtCore.QVariant('No {0}'.format(section))
        elif role == QtCore.Qt.TextAlignmentRole:
            # and the alignment
            return QtCore.QVariant(QtCore.Qt.AlignRight)
        else:
            return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            # the text to display!
            return QtCore.QVariant(DATA[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            # the alignment of the cell
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        else:
            return QtCore.QVariant()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        splitter = QtGui.QSplitter(self)
        left = QtGui.QWidget(splitter)
        left.setLayout(QtGui.QVBoxLayout(left))
        left.layout().addWidget(QtGui.QLabel('QTableView', left))
        tableview = QtGui.QTableView(left)
        tableview.setModel(TableModel(tableview))
        left.layout().addWidget(tableview)
        splitter.addWidget(left)
        right = QtGui.QWidget(splitter)
        right.setLayout(QtGui.QVBoxLayout(right))
        right.layout().addWidget(QtGui.QLabel('QTableWidget', right))
        # create a table widget for DATA
        tablewidget = QtGui.QTableWidget(len(DATA), len(DATA[1]), right)
        right.layout().addWidget(tablewidget)
        splitter.addWidget(right)
        self.setCentralWidget(splitter)

        # add tablewidget data
        self.add_data(tablewidget)

    def add_data(self, widget):
        # delete vertical headers
        for i in xrange(widget.rowCount()):
            widget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem())
        # set horizontal headers
        for i in xrange(widget.columnCount()):
            # the text
            item = QtGui.QTableWidgetItem('No {0}'.format(i))
            # the alignment
            item.setTextAlignment(QtCore.Qt.AlignRight)
            widget.setHorizontalHeaderItem(i, item)
        # set data
        for y, row in enumerate(DATA):
            for x, cell in enumerate(row):
                # the text
                item = QtGui.QTableWidgetItem(cell)
                # the alignment
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                widget.setItem(y, x, item)


def main():
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
