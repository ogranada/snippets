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


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtGui import (QMainWindow, QWidget, QHBoxLayout, QAction, QStyle,
                          QFileDialog, QApplication)
from PySide.phonon import Phonon


class MainWindow(QMainWindow):

    ACTIONS = [
        ('ask_open_filename', 'Open', QStyle.SP_DialogOpenButton),
        ('play', 'Play', QStyle.SP_MediaPlay),
        ('pause', 'Pause', QStyle.SP_MediaPause),
        ('stop', 'Stop', QStyle.SP_MediaStop),
        ('copy_to_right_video', 'Copy video to right', None),
        ('remove_right_video', 'Remove right video', None)
    ]


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # create two video widgets
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
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

        self.actions_toolbar = self.addToolBar('Actions')
        self._actions = {}
        for name, label, icon_name in self.ACTIONS:
            if icon_name:
                icon = self.style().standardIcon(icon_name)
                action = QAction(icon, label, self)
            else:
                action = QAction(label, self)
            action.setObjectName(name)
            if name in ('play', 'pause', 'stop'):
                action.triggered.connect(getattr(self.media, name))
            else:
                action.triggered.connect(getattr(self, name))
            self.actions_toolbar.addAction(action)
        self._action('remove_right_video').setEnabled(False)

    def _action(self, name):
        return self.findChild(QAction, name)

    def copy_to_right_video(self):
        if not self.right_path:
            self.right_path = Phonon.createPath(self.media, self.right_video)
            self._action('copy_to_right_video').setEnabled(False)
            self._action('remove_right_video').setEnabled(True)

    def remove_right_video(self):
        if self.right_path:
            if self.right_path.disconnectPath():
                self.right_path = None
                self._action('copy_to_right_video').setEnabled(True)
                self._action('remove_right_video').setEnabled(False)

    def ask_open_filename(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open video ...', '', 'AVI Files (*.avi);;All files (*)')
        if filename:
            # load (but don't play!) the given filename
            self.media.setCurrentSource(Phonon.MediaSource(filename))

    def closeEvent(self, event):
        # stop video and audio playback, if the window is closed
        self.media.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()

