# -*- coding: utf-8 -*-


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

