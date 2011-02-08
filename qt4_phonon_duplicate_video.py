#!/usr/bin/python
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
    qt4_phonon_duplicate_video
    ==========================



    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

import sys

from PyQt4 import QtGui
from PyQt4.phonon import Phonon


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        # create two video widgets
        central = QtGui.QWidget(self)
        self.setCentralWidget(central)
        layout = QtGui.QHBoxLayout(central)
        central.setLayout(layout)
        self.left_video = Phonon.VideoWidget(self)
        self.right_video = Phonon.VideoWidget(self)
        layout.addWidget(self.left_video)
        layout.addWidget(self.right_video)

        # the media object controlling the video playback
        self.media = Phonon.MediaObject(self)
        # the audio sink
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self);
        # connect the media object with audio and *left* video
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.left_video)
        # holds the Path object, that connects self.media with self.right_video
        self.right_path = None

        self.actions = self.addToolBar('Actions')
        # some actions for control
        self.open = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_DialogOpenButton), 'Open', self)
        self.open.setObjectName('open')
        self.play = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaPlay), 'Play', self)
        self.pause = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaPause), 'Pause', self)
        self.stop = QtGui.QAction(self.style().standardIcon(
            QtGui.QStyle.SP_MediaStop), 'Stop', self)
        self.copy = QtGui.QAction('Copy video to right', self)
        self.uncopy = QtGui.QAction('Remove right video', self)
        self.uncopy.setEnabled(False)
        # add actions to the toolbar
        for act in (self.open, self.play, self.pause, self.stop,
                    self.copy, self.uncopy):
            self.actions.addAction(act)
        # connect the signals
        self.play.triggered.connect(self.media.play)
        self.pause.triggered.connect(self.media.pause)
        self.stop.triggered.connect(self.media.stop)
        self.open.triggered.connect(self.ask_open_video)
        self.copy.triggered.connect(self.copy_to_right_video)
        self.uncopy.triggered.connect(self.remove_right_video)

    def copy_to_right_video(self):
        if not self.right_path:
            self.right_path = Phonon.createPath(self.media, self.right_video)
            self.copy.setEnabled(False)
            self.uncopy.setEnabled(True)

    def remove_right_video(self):
        if self.right_path:
            if self.right_path.disconnect():
                self.right_path = None
                self.copy.setEnabled(True)
                self.uncopy.setEnabled(False)

    def ask_open_video(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open video ...', '', 'AVI Files (*.avi);;All files (*)')
        if filename:
            # load (but don't play!) the given filename
            self.media.setCurrentSource(Phonon.MediaSource(filename))

    def closeEvent(self, evt):
        # stop video and audio playback, if the window is closed
        self.media.stop()
        super(QtGui.QMainWindow, self).closeEvent(evt)


def main():
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()

