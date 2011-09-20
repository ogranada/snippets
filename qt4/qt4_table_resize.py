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
    qt4_table_resize
    ================

    Demonstrates how to derive from QTableView to resize columns, wenn the
    view is resized.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide.QtGui import QMainWindow, QTableView, QApplication


class SimpleTableModel(QAbstractTableModel):
    """Simple model for the demonstration purposes."""

    def __init__(self, table, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.table = table

    def rowCount(self, parent=QModelIndex()):
        return len(self.table)

    def columnCount(self, parent=QModelIndex()):
        return max(len(row) for row in self.table)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role != Qt.DisplayRole or not index.isValid():
            return
        try:
            return self.table[index.row()][index.column()]
        except IndexError:
            return 0


class AutoSizeTableView(QTableView):
    """
    A subclass of QTableView, which resizes its columns automatically, if
    the :attr:`auto_resize_columns` attribute is ``True``.
    """

    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.auto_resize_columns = False

    def resizeEvent(self, evt):
        if self.auto_resize_columns:
            # determine the size of the displayed area of the table
            size = self.viewport().size()
            # calculate the size of each individual column.  This is a
            # rather simple way, in a real application the current size of
            # any column should be used to resize the columns in a way, that
            # preserves the size distribution among all columns.
            width = size.width() / self.model().columnCount()
            # adjust the size of each column
            for col in xrange(self.model().columnCount()):
                self.setColumnWidth(col, width)
        # call the base class
        super(QTableView, self).resizeEvent(evt)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Table test')
        view = AutoSizeTableView(self)
        view.auto_resize_columns = True
        model = SimpleTableModel([['foo', 'bar'], ['spam', 'eggs']], view)
        view.setModel(model)
        self.setCentralWidget(view)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

