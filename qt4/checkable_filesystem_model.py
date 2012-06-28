#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011 Sebastian Wiesner <lunaryorn@gmail.com>

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
    Implementation of a QFileSystemModel-derived model, which adds check
    boxes to each file.  Demonstrates some more advanced model-view
    techniques.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
import os
from xml.sax.saxutils import escape

from PySide.QtCore import Qt
from PySide.QtGui import (QFileSystemModel, QListView, QMainWindow,
                          QAction, QStyle, QApplication, QFileDialog,
                          QMessageBox)


class CheckableFilesystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        QFileSystemModel.__init__(self, parent)
        self._checked_files = set()
        self.fileRenamed.connect(self._updateOnRename)
        self.rootPathChanged.connect(self._updateOnRootPathChange)

    @property
    def checked_files(self):
        return sorted(self._checked_files)

    def flags(self, index):
        return QFileSystemModel.flags(self, index) | Qt.ItemIsUserCheckable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.CheckStateRole:
            filename = self.data(index, QFileSystemModel.FileNameRole)
            if filename:
                return (Qt.Checked
                        if filename in self._checked_files
                        else Qt.Unchecked)
        return QFileSystemModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            filename = self.data(index, QFileSystemModel.FileNameRole)
            if value == Qt.Checked:
                self._checked_files.add(filename)
            else:
                self._checked_files.discard(filename)
            return True
        return QFileSystemModel.setData(self, index, value, role)

    def _updateOnRename(self, path, oldname, newname):
        oldname = unicode(oldname)
        newname = unicode(newname)
        if oldname in self._checked_files:
            self._checked_files.remove(oldname)
            self._checked_files.add(newname)

    def _updateOnRootPathChange(self):
        self._checked_files.clear()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.view = QListView(self)
        self.view.setModel(CheckableFilesystemModel(self.view))
        self.view.activated.connect(self.openIndex)
        self.setCentralWidget(self.view)
        open_action = QAction(self.style().standardIcon(
            QStyle.SP_DialogOpenButton), 'Open', self)
        open_action.triggered.connect(self.askOpenDirectory)
        show_action = QAction('Show checked filenames', self)
        show_action.triggered.connect(self.showCheckedFiles)
        actions = self.addToolBar('Actions')
        actions.addAction(open_action)
        actions.addAction(show_action)
        self.openDirectory(os.path.expanduser('~'))

    def askOpenDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            self, 'Open directory ...', os.path.expanduser('~'))
        if directory:
            self.openDirectory(directory)

    def openDirectory(self, directory):
        if os.path.isdir(directory):
            root = self.view.model().setRootPath(directory)
            self.view.setRootIndex(root)

    def openIndex(self, index):
        model = self.view.model()
        directory = model.data(index, QFileSystemModel.FilePathRole)
        self.openDirectory(directory)

    def showCheckedFiles(self):
        checked_files = self.view.model().checked_files
        if checked_files:
            print('\n'.join(checked_files))
            filelist = ''.join('<li>{0}</li>'.format(escape(fn))
                               for fn in checked_files)
            QMessageBox.information(self, 'Checked files',
                                    '<ul>{0}</ul>'.format(filelist),)
        else:
            print('no files checked')
            QMessageBox.information(self, 'No files checked',
                                    'No files checked')


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
