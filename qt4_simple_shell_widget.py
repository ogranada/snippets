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
    qt4_simple_shell_widget
    =======================

    A *very* simple shell widget using QProcess.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys

from PyQt4.QtCore import QProcess, QString, SIGNAL
from PyQt4.QtGui import QPlainTextEdit, QApplication


class QSimpleShellWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.setReadOnly(True)
        self.process = None

    def setProcess(self, process):
        self.clear()
        self.process = process
        self.connect(process, SIGNAL('readyReadStandardError()'),
                     self.read_output)
        self.connect(process, SIGNAL('readyReadStandardOutput()'),
                     self.read_output)

    def read_output(self):
        stdout = QString(self.process.readAllStandardOutput())
        stderr = QString(self.process.readAllStandardError())
        self.appendPlainText(stderr)
        self.appendPlainText(stdout)


def main():
    app = QApplication(sys.argv)
    window = QSimpleShellWidget()
    proc = QProcess()
    window.setProcess(proc)
    proc.start('sh -c "while true; do echo foo; sleep 1; done"')
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

