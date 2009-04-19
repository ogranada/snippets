#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QApplication, QMainWindow, QMenu, QAction


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowState(Qt.WindowFullScreen | Qt.WindowActive)
        self.setCursor(Qt.BlankCursor)
        appmenu = QMenu('&Application', self)
        quit = QAction('&Quit', self)
        appmenu.addAction(quit)
        self.menuBar().addMenu(appmenu)
        self.connect(quit, SIGNAL('triggered()'),
                     QApplication.instance().quit)


def main():
    app = QApplication(sys.argv)
    mywindow = MyMainWindow()
    mywindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
