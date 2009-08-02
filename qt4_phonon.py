#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

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
    qt4_phonon
    ==========

    Implementation of a simple video player using the Qt4 phonon multimedia
    framework.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        # create the video player
        self.player = Phonon.VideoPlayer(self)
        self.setCentralWidget(self.player)
        self.actions = self.addToolBar('Actions')
        # create some actions to open and play video files
        self.open = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_DialogOpenButton), 'Open', self)
        self.open.setObjectName('open')
        self.play = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaPlay), 'Play', self)
        self.pause = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaPause), 'Pause', self)
        self.stop = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaStop), 'Stop', self)
        # add the actions to the toolbar
        self.actions.addAction(self.open)
        self.actions.addAction(self.play)
        self.actions.addAction(self.pause)
        self.actions.addAction(self.stop)
        # and connect them with the player
        QtCore.QMetaObject.connectSlotsByName(self)
        self.connect(self.play, QtCore.SIGNAL('triggered()'),
                     self.player.play)
        self.connect(self.pause, QtCore.SIGNAL('triggered()'),
                     self.player.pause)
        self.connect(self.stop, QtCore.SIGNAL('triggered()'),
                     self.player.stop)

    @QtCore.pyqtSignature('')
    def on_open_triggered(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open video ...', '', 'AVI Files (*.avi);;All files (*)')
        if filename:
            # load (but don't play!) the given filename
            self.player.load(Phonon.MediaSource(filename))


def main():
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
