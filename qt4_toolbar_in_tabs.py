#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


class ToolbarTabWidget(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

    def setupUi(self):
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction('eggs')



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Tab Test')
        self.tabs = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tabs)
        tab = ToolbarTabWidget()
        self.tabs.addTab(tab, 'spam')


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
