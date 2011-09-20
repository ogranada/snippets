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
    Implementation of a simple audio player using the Phonon framework from
    Qt4.  Requires at least Python 2.6 and Qt 4.5.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.phonon import Phonon
from PySide.QtGui import (QApplication, QMainWindow, QAction, QStyle,
                          QFileDialog)


class PlaybackWindow(QMainWindow):

    # gui messages for different playback states
    STATE_MESSAGES = {
        Phonon.LoadingState: 'Loading {filename}',
        Phonon.ErrorState: 'Error occured: {error}',
        Phonon.PausedState: 'Paused {filename}',
        Phonon.PlayingState: 'Playing {filename}',
        Phonon.StoppedState: 'Stopped {filename}',
        Phonon.BufferingState: 'Buffering'}

    ACTIONS = [
        ('open', 'Open', QStyle.SP_DialogOpenButton),
        ('play', 'Play', QStyle.SP_MediaPlay),
        ('pause', 'Pause', QStyle.SP_MediaPause),
        ('stop', 'Stop', QStyle.SP_MediaStop),
    ]

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowFilePath('No file')
        # the media object controls the playback
        self.media = Phonon.MediaObject(self)
        # the audio output does the actual sound playback
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        # a slider to seek to any given position in the playback
        self.seeker = Phonon.SeekSlider(self)
        self.setCentralWidget(self.seeker)
        # link media objects together.  The seeker will seek in the created
        # media object
        self.seeker.setMediaObject(self.media)
        # audio data from the media object goes to the audio output object
        Phonon.createPath(self.media, self.audio_output)
        # set up actions to control the playback
        self.actions = self.addToolBar('Actions')
        for name, label, icon_name in self.ACTIONS:
            icon = self.style().standardIcon(icon_name)
            action = QAction(icon, label, self)
            action.setObjectName(name)
            self.actions.addAction(action)
            if name == 'open':
                action.triggered.connect(self._ask_open_filename)
            else:
                action.triggered.connect(getattr(self.media, name))
        # whenever the playback state changes, show a message to the user
        self.media.stateChanged.connect(self._show_state_message)

    def _ask_open_filename(self):
        # ask the user for a filename
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open audio file ...', '',
            'Audio Files (*.mp3 *.ogg *.wav);;All files (*)')
        if filename:
            # load (but don't play!) the file
            self.media.setCurrentSource(Phonon.MediaSource(filename))

    def _show_state_message(self, new_state):
        # get the message for the given state and format it
        message = self.STATE_MESSAGES[new_state].format(
            filename=self.media.currentSource().fileName(),
            error=self.media.errorString())
        self.statusBar().showMessage(message)
        # set the file path in the window title bar, if the playback source
        # is a local file
        source = self.media.currentSource()
        filepath = 'No File'
        if source.type() == Phonon.MediaSource.LocalFile:
            filepath = source.fileName()
        self.setWindowFilePath(filepath)


def main():
    app = QApplication(sys.argv)
    # this is used for the window title
    app.setApplicationName('PoC audio player')
    mainwindow = PlaybackWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
