#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Christian Hausknecht

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""
    progressthread
    ==============

    Simple module to demonstrate how to use the QThread class in order to
    integrate longer processes within a GUI.

    :author: Christian Hausknecht
    :copyright: 2010 by Christian Hausknecht
    :contact: christian.hausknecht@gmx.de
    :license: WTFPL
"""

__author__ = "Christian Hausknecht"


import sys
from PyQt4 import QtGui, uic, QtCore, Qt
from time import sleep


class Counter(QtCore.QThread):

    count = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QtCore.QThread.__init__(self)

    def run(self):
        for i in range(1, 101):
            self.count.emit(i)
            sleep(0.1)


class MyMainWidget(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("qt4_thread_progress.ui", self)
        self.counter = Counter(self)

        self.startButton.clicked.connect(self.slot_start)
        self.counter.finished.connect(self.slot_done)
        self.counter.count.connect(self.slot_count)

    def slot_start(self):
        self.textBrowser.append(u"Zähle bis 100")
        self.counter.start()

    def slot_done(self):
        self.textBrowser.append(u"fertisch :-)")

    def slot_count(self, count):
        self.progressBar.setValue(count)
        self.textBrowser.append(str(count))


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MyMainWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
