# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt4.QtGui import QMainWindow, QTableView, QApplication


class SimpleTableModel(QAbstractTableModel):

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
            return QVariant()
        try:
            return QVariant(
                self.table[index.row()][index.column()])
        except IndexError:
            return QVariant(0)


class AutoSizeTableView(QTableView):

    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.auto_resize_columns = False

    def resizeEvent(self, evt):
        if self.auto_resize_columns:
            size = self.viewport().size()
            width = size.width() / self.model().columnCount()
            for col in xrange(self.model().columnCount()):
                self.setColumnWidth(col, width)
        QTableView.resizeEvent(self, evt)


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

