#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2008 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    qt_service_manager
    ==================

    A Qt4 Gui implementing a simple service manager for Gentoo.


    :author: Sebastian Wiesner
    :contact: lunaryorn@googlemail.com
    :copyright: 2008 by Sebastian Wiesner
    :license: MIT
"""


import re
import sys

from PyQt4 import QtCore, QtGui


class ServiceManagerMainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Qt Service Manager')
        self.servicemanager = ServiceManagerWidget()
        self.setCentralWidget(self.servicemanager)
        self.connect(self.servicemanager.quit_button,
                     QtCore.SIGNAL('clicked()'), self.close)
        self.servicemanager.directory_view.setMouseTracking(True)
        self.connect(
            self.servicemanager.directory_view,
            QtCore.SIGNAL('entered(const QModelIndex &)'),
            self.service_status)
        # create the status bar
        #self.statusBar()

    def service_status(self, index):
        service = self.servicemanager.directory_model.filePath(index)
        status = self.servicemanager.service_status(service) or 'Unknown'
        self.statusBar().showMessage('Status: %s' % status)


class ServiceManagerWidget(QtGui.QWidget):
    """Implements a widget, which allows to manage services on Gentoo."""
    service_status_pattern = re.compile(r'^ \* status: {2}(?P<status>\w*)$')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.directory_model = QtGui.QDirModel(self)
        self.directory_model.setFilter(
            QtCore.QDir.Executable | QtCore.QDir.Files)
        self.directory_model.setSorting(QtCore.QDir.Name)
        layout = QtGui.QVBoxLayout(self)
        self.directory_view = QtGui.QTreeView(self)
        self.directory_view.setModel(self.directory_model)
        self.directory_view.setRootIndex(
            self.directory_model.index('/etc/init.d/'))
        layout.addWidget(self.directory_view)
        button_layout = QtGui.QHBoxLayout()
        self.quit_button = QtGui.QPushButton('Quit')
        start_button = QtGui.QPushButton('Start')
        stop_button = QtGui.QPushButton('Stop')
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(self.quit_button)
        self.connect(start_button, QtCore.SIGNAL('clicked()'),
                     self.start_service)
        self.connect(stop_button, QtCore.SIGNAL('clicked()'),
                     self.stop_service)
        layout.addLayout(button_layout)
        # watch the service dir for changed
        watcher = QtCore.QFileSystemWatcher(['/etc/init.d'], self)
        self.connect(
            watcher, QtCore.SIGNAL('directoryChanged( const QString & )'),
            self.directory_model.refresh)

    def get_selected_service(self):
        """Returns the path of the currently selected service."""
        selected = self.directory_view.selectedIndexes()
        if selected:
            return self.directory_model.filePath(selected[0])

    def call_service(self, service, action):
        """Calls `service` to perform `action`."""
        proc = QtCore.QProcess(self)
        proc.start(service, [action])
        return proc

    def start_service(self):
        service = self.get_selected_service()
        self.call_service(service, 'start')

    def stop_service(self):
        service = self.get_selected_service()
        self.call_service(service, 'stop')

    def service_status(self, service):
        """Determines the status of `service`. Returns a string describing
        the status, or None, if the status couldn't be determined.
        """
        proc = self.call_service(service, 'status')
        print service
        if proc.waitForFinished(3000):
            output = str(proc.readAllStandardOutput())
            res = self.service_status_pattern.match(output)
            if res:
                return res.group('status')
        return None


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Qt Service Manager')
    mainwindow = ServiceManagerMainWindow()
    mainwindow.setVisible(True)
    app.exec_()


if __name__ == '__main__':
    main()

