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
    qt4_countdown
    =============

    A little countdown clock implemented with QTime and QTimer.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys

from PyQt4.QtCore import Qt, SIGNAL, QTime, QTimer
from PyQt4.QtGui import QApplication, QLabel


class CountdownWidget(QLabel):
    def __init__(self, countdown, parent=None):
        QLabel.__init__(self, parent)
        self.countdown = countdown
        self.setText(self.countdown.toString(Qt.ISODate))
        # setup the countdown timer
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'),
                     self._update)

    def start(self):
        # update the display every second
        self.timer.start(1000)

    def _update(self):
        # this gets called every seconds
        # adjust the remaining time
        self.countdown = self.countdown.addSecs(-1)
        # if the remaining time reached zero, stop the timer
        if self.countdown <= QTime(0, 0, 0):
            self.timer.stop()
        # update the display
        self.setText(self.countdown.toString(Qt.ISODate))


def main():
    app = QApplication(sys.argv)
    widget = CountdownWidget(QTime(0, 0, 5))
    widget.start()
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
