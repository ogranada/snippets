#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011 Christian Hausknecht <christian.hausknecht@gmx.de>
# Copyright (c) 2010 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    qt4_thread_progress
    ===================

    Demonstrates how to use QThread together with QProgressBar to report the
    progress of background worker threads for longer running processes in a
    GUI.

    Based on work of Christian Hausknecht as presented in a posting_ in the
    german Python forum.  Much thanks for his efforts :)

    .. _posting: http://www.python-forum.de/viewtopic.php?f=11&t=24036

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
    .. moduleauthor::  Christian Hausknecht <christian.hausknecht@gmx.de>
"""


import sys
from functools import partial

from PySide.QtCore import QThread, QSemaphore, Signal
from PySide.QtGui import (QApplication, QMainWindow, QWidget, QPlainTextEdit,
                          QProgressBar, QAction, QVBoxLayout, QIcon)


class Counter(QThread):

    #: this signal is emitted whenever the worker has performed a single
    #  step
    progress = Signal(int)
    #: this signal publishes the minimum amount of required steps
    minimumChanged = Signal(int)
    #: this signal publishes the maximum amount of required steps
    maximumChanged = Signal(int)

    def __init__(self, maximum, parent=None):
        QThread.__init__(self, parent)
        self.maximum = maximum
        # this semaphore is used to stop the thread from outside.  As long
        # as the thread is permitted to run, it has yet a single resource
        # available.  If the thread is stopped, this resource is acquired,
        # and the thread breaks its counting loop at the next iteration.
        self._run_semaphore = QSemaphore(1)

    def run(self):
        # published our minimum and maximum values.  A real worker thread
        # would typically calculate the number of required steps
        self.minimumChanged.emit(1)
        self.maximumChanged.emit(self.maximum)
        # now do our work, which is simply counting in this example
        for i in range(1, self.maximum+1):
            self.progress.emit(i)
            # check, if the thread is still permitted to run.  This test
            # fails, if the single resource of this semaphore is acquired,
            # which is done by the stop() method, just to stop work at
            # precisly this point
            if self._run_semaphore.available() == 0:
                # release the resource again to enable a restart of this worker
                self._run_semaphore.release(1)
                # break the loop.  A real worker would typically roll back
                # his work to leave the state of the application unchanged,
                # because the work was forcibly interrupted.
                break
            # simulate some heavy work
            self.msleep(100)

    def stop(self):
        # acquire the single resource of our run semaphore.  No resources
        # are now available anymore, so next time, run() checks the number
        # of available resources, it sees none and returns.
        self._run_semaphore.acquire(1)


class CountingMainWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # the user interface, consisting of a progress bar above a plain
        # text edit, which logs all actions.
        container = QWidget(self)
        container.setLayout(QVBoxLayout(container))
        self.setCentralWidget(container)
        progressbar = QProgressBar(container)
        container.layout().addWidget(progressbar)
        log = QPlainTextEdit(container)
        container.layout().addWidget(log)

        # the actual worker thread
        counter = Counter(100, self)

        # an action to quit the windows
        exit = QAction(QIcon.fromTheme('application-exit'), 'exit', self)

        # add two actions to start and stop the worker to the toolbar of the
        # main window
        start_counting = QAction(QIcon.fromTheme('media-playback-start'),
                                 'Start counting', self)
        stop_counting = QAction(QIcon.fromTheme('media-playback-stop'),
                                'Stop counting', self)
        # initially no counter runs, so we can disable the stop action
        stop_counting.setEnabled(False)

        # add all actions to a toolbar
        actions = self.addToolBar('Actions')
        actions.addAction(exit)
        actions.addSeparator()
        actions.addAction(start_counting)
        actions.addAction(stop_counting)

        # quit the application, if the quit action is triggered
        exit.triggered.connect(QApplication.instance().quit)

        # start and stop the counter, if the corresponding actions are
        # triggered.
        start_counting.triggered.connect(counter.start)
        stop_counting.triggered.connect(counter.stop)

        # adjust the minimum and the maximum of the progress bar, if
        # necessary.  Not really required in this snippet, but added for the
        # purpose of demonstrating it
        counter.minimumChanged.connect(progressbar.setMinimum)
        counter.maximumChanged.connect(progressbar.setMaximum)

        # switch the enabled states of the actions according to whether the
        # worker is running or not
        counter.started.connect(partial(start_counting.setEnabled, False))
        counter.started.connect(partial(stop_counting.setEnabled, True))
        counter.finished.connect(partial(start_counting.setEnabled, True))
        counter.finished.connect(partial(stop_counting.setEnabled, False))

        # update the progess bar continuously
        counter.progress.connect(progressbar.setValue)

        # log all actions in our logging widget
        counter.started.connect(
            partial(self.statusBar().showMessage, 'Counting'))
        counter.finished.connect(
            partial(self.statusBar().showMessage, 'Done'))
        # log a forced stop
        stop_counting.triggered.connect(
            partial(log.appendPlainText, 'Stopped'))
        # log all counted values
        counter.progress.connect(lambda v: log.appendPlainText(str(v)))

        # and finally show the current state in the status bar.
        counter.started.connect(partial(log.appendPlainText, 'Counting'))
        counter.finished.connect(partial(log.appendPlainText, 'Done'))


def main():
    app = QApplication(sys.argv)
    widget = CountingMainWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
