#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009, 2011 Sebastian Wiesner <lunaryorn@gmail.com>

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
    Implementation of a simple video player using the Qt4 phonon multimedia
    framework.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtGui import (QApplication, QMainWindow, QAction, QStyle,
                          QFileDialog)
from PySide.phonon import Phonon


class MainWindow(QMainWindow):

    ACTIONS = [
        ('open', 'Open', QStyle.SP_DialogOpenButton),
        ('play', 'Play', QStyle.SP_MediaPlay),
        ('pause', 'Pause', QStyle.SP_MediaPause),
        ('stop', 'Stop', QStyle.SP_MediaStop),
    ]

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowFilePath('No file')
        # create the video player
        self.player = Phonon.VideoPlayer(self)
        self.setCentralWidget(self.player)
        self.actions = self.addToolBar('Actions')
        # create some actions to open and play video files
        for name, label, icon_name in self.ACTIONS:
            icon = self.style().standardIcon(icon_name)
            action = QAction(icon, label, self)
            action.setObjectName(name)
            if name == 'open':
                action.triggered.connect(self._ask_open_filename)
            else:
                action.triggered.connect(getattr(self.player, name))
            self.actions.addAction(action)

    def _ask_open_filename(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open video ...', '', 'AVI Files (*.avi);;All files (*)')
        if filename:
            # load (but don't play!) the given filename
            self.player.load(Phonon.MediaSource(filename))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('PoC video player')
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
