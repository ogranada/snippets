# -*- coding: utf-8 -*-


import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Model(QAbstractListModel):
    def __init__(self, pages, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.pages = pages

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            name, icon = self.pages[index.row()]
            if role == Qt.DisplayRole:
                return QVariant(name)
            elif role == Qt.DecorationRole and icon:
                return QVariant(icon)
        return QVariant()

    def rowCount(self, index):
        return len(self.pages)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setup_ui()

    def find_icon(self, name):
        path = os.path.join(
            '/usr/share/icons/oxygen/scalable/categories', name + '.svgz')
        if os.path.isfile(path):
            return QIcon(path)
        else:
            return None

    def setup_ui(self):
        view = QListView(self)
        view.setViewMode(QListView.IconMode)
        view.setMovement(QListView.Static)
        view.setIconSize(QSize(64, 64))
        pages = [
            ('System', self.find_icon('preferences-system')),
            ('Desktop', self.find_icon('preferences-desktop-personal'))]
        model = Model(pages, self)
        view.setModel(model)
        self.setCentralWidget(view)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

