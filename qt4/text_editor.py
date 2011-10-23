#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

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

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

__version__ = '0.1'

import sys
import os
from functools import partial
from codecs import open

from PySide.QtUiTools import QUiLoader
from PySide.QtCore import Property, QSettings
from PySide.QtGui import (QApplication, QMainWindow,
                          QFileDialog, QInputDialog, QMessageBox,
                          QPrintPreviewDialog, QLabel,
                          QAction, QKeySequence, QIcon,
                          QTextDocument, QTextCursor,
                          QDesktopServices)


APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]


class UiLoader(QUiLoader):
    def __init__(self, baseinstance):
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None:
            return self.baseinstance
        else:
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            setattr(self.baseinstance, name, widget)
            return widget


class TextEditor(QMainWindow):

    ACTION_PREFIX = 'action'

    ACTION_ICONS = dict(
        New='document-new',
        Open='document-open',
        Save='document-save',
        SaveAs='document-save-as',
        Print='document-print',
        Quit='application-exit',
        Undo='edit-undo',
        Redo='edit-redo',
        Cut='edit-cut',
        Copy='edit-copy',
        Paste='edit-paste',
        Find='edit-find',
        FindNext='go-down',
        FindPrevious='go-up',
        SelectAll='edit-select-all',
    )

    ACTION_KEYS = dict(
        New=QKeySequence.New,
        Open=QKeySequence.Open,
        Save=QKeySequence.Save,
        SaveAs=QKeySequence.SaveAs,
        Print=QKeySequence.Print,
        Quit=QKeySequence.Quit,
        Undo=QKeySequence.Undo,
        Redo=QKeySequence.Redo,
        Cut=QKeySequence.Cut,
        Copy=QKeySequence.Copy,
        Paste=QKeySequence.Paste,
        Find=QKeySequence.Find,
        FindNext=QKeySequence.FindNext,
        FindPrevious=QKeySequence.FindPrevious,
        SelectAll=QKeySequence.SelectAll,
    )

    DISABLED_ACTIONS = set(['Save', 'Undo', 'Redo'])

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uifile = os.path.join(APP_DIRECTORY, MODULE_NAME+'.ui')
        loader = UiLoader(self)
        loader.load(uifile)
        # unset the window title to enable the automatic window title
        # constructed from windowFilePath and windowModified
        self.setWindowTitle('')
        self.setupActions()
        self.setupEditor()
        self.setupStatusBar()
        self.setupSearchDock()
        self.settings = QSettings(self)
        self.loadSettings()

    def setupActions(self):
        action_slots = dict(
            New=self.newFile, Open=self.askOpenFile, Save=self.saveFile,
            SaveAs=self.askSaveFile, Print=self.askPrint, Quit=self.close,
            Undo=self.editor.undo, Redo=self.editor.redo, Cut=self.editor.cut,
            Copy=self.editor.copy, Paste=self.editor.paste,
            Find=self.toggleSearchDock, FindNext=self.find,
            FindPrevious=partial(self.find, backwards=True),
            SelectAll=self.editor.selectAll, GoToLine=self.askGoToLine,
            AboutQt=QApplication.instance().aboutQt, About=self.about)
        for action in self.findChildren(QAction):
            object_name = action.objectName()
            if not object_name:
                continue
            action_name = object_name[len(self.ACTION_PREFIX):]
            icon_name = self.ACTION_ICONS.get(action_name)
            if icon_name:
                action.setIcon(QIcon.fromTheme(icon_name))
            key = self.ACTION_KEYS.get(action_name)
            if key:
                action.setShortcut(key)
            slot = action_slots.get(action_name)
            if slot:
                action.triggered.connect(slot)
            if action_name in self.DISABLED_ACTIONS:
                action.setEnabled(False)
        for action in self.menuEdit.actions():
            self.editor.addAction(action)

    def setupEditor(self):
        self.editor.cursorPositionChanged.connect(self.updateStatusBar)
        self.editor.modificationChanged.connect(self.setWindowModified)
        self.editor.modificationChanged.connect(self.actionSave.setEnabled)
        self.editor.undoAvailable.connect(self.actionUndo.setEnabled)
        self.editor.redoAvailable.connect(self.actionRedo.setEnabled)

    def setupStatusBar(self):
        self.cursorPositionLabel = QLabel(self.statusBar())
        self.statusBar().addPermanentWidget(self.cursorPositionLabel)

    def setupSearchDock(self):
        self.searchDock.hide()
        self.findNext.setDefaultAction(self.actionFindNext)
        self.findPrevious.setDefaultAction(self.actionFindPrevious)

    def loadSettings(self):
        self.restoreGeometry(self.settings.value('texteditor/geoemtry') or b'')
        self.restoreState(self.settings.value('texteditor/state') or b'')
        self.searchCaseSensitive.setChecked(
            self.settings.value('search/case_sensitive', False)=='true')

    def saveSettings(self):
        self.settings.setValue('texteditor/geoemtry', self.saveGeometry())
        self.settings.setValue('texteditor/state', self.saveState())
        self.settings.setValue('search/case_sensitive',
                               self.searchCaseSensitive.isChecked())

    @Property(unicode)
    def currentFilename(self):
        return self.editor.document().metaInformation(
            QTextDocument.DocumentUrl)

    @currentFilename.setter
    def setCurrentFilename(self, filename):
        self.editor.document().setMetaInformation(
            QTextDocument.DocumentUrl, filename)
        self.setWindowFilePath(filename or self.trUtf8('untitled'))

    def save(self, filename=None):
        filename = filename or self.currentFilename
        if not filename:
            raise ValueError()
        try:
            encoding = sys.getfilesystemencoding()
            with open(filename, 'w', encoding=encoding) as stream:
                stream.write(self.editor.toPlainText())
        except EnvironmentError as error:
            QMessageBox.critical(self, self.trUtf8(b'Save file'), self.trUtf8(
                b'Could not save <tt>{filename}</tt>: {message}').format(
                    filename=filename, message=error.strerror))
            return False
        else:
            self.editor.document().setModified(False)
            self.currentFilename = filename
            return True

    def load(self, filename):
        try:
            encoding = sys.getfilesystemencoding()
            with open(filename, 'r', encoding=encoding) as stream:
                self.editor.setPlainText(stream.read())
            self.currentFilename = filename
            return True
        except EnvironmentError as error:
            QMessageBox.critical(self, self.trUtf8('Open file'), self.trUtf8(
                b'Could not open <tt>{filename}</tt>: {message}').format(
                    filename=filename, message=error.strerror))
            return False

    def print(self, printer):
        printer.setDocName(self.windowFilePath())
        self.editor.print_(printer)

    def goToLine(self, line):
        block = self.editor.document().findBlockByLNumber(line)
        cursor = QTextCursor(self.editor.document())
        cursor.setPosition(block.position())
        self.editor.setTextCursor(cursor)

    def updateStatusBar(self):
        cursor = self.editor.textCursor()
        cursor_position = self.trUtf8(b'({line},{column},{offset})').format(
            line=cursor.blockNumber(), column=cursor.columnNumber(),
            offset=cursor.position())
        self.cursorPositionLabel.setText(cursor_position)

    def askSaveChanges(self):
        if self.editor.document().isModified():
            response = QMessageBox.warning(
                self, self.trUtf8(b'Save changes?'),
                self.trUtf8(b'The document has been modified.\n'
                            'Do you want to save your changes?'),
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save)
            if response == QMessageBox.Cancel:
                return False
            if response == QMessageBox.Save:
                return self.saveFile()
        return True

    def newFile(self):
        if not self.askSaveChanges():
            return
        self.editor.clear()
        self.currentFilename = None
        self.setWindowModified(False)
        self.actionSave.setEnabled(False)

    def saveFile(self):
        if self.currentFilename:
            return self.save()
        else:
            return self.askSaveFile()

    def askSaveFile(self):
        if self.currentFilename:
            directory = os.path.dirname(self.currentFilename)
        else:
            directory = QDesktopServices.storageLocation(
                QDesktopServices.DocumentsLocation)
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, self.trUtf8(b'Save file'), directory)
        if not filename:
            return False
        return self.saveFile()

    def askOpenFile(self):
        if not self.askSaveChanges():
            return
        directory = QDesktopServices.storageLocation(
            QDesktopServices.DocumentsLocation)
        filename, selected_filter = QFileDialog.getOpenFileName(
            self, self.trUtf8(b'Open file'), directory)
        if filename:
            self.load(filename)

    def askGoToLine(self):
        line, ok = QInputDialog.getInt(
            self, self.trUtf8(b'Goto line'), self.trUtf8(b'Line number:'),
            self.editor.textCursor().blockNumber(), 1,
            self.editor.document().blockCount())
        if ok:
            self.goToLine(line)

    def askPrint(self):
        dialog = QPrintPreviewDialog(self)
        dialog.paintRequested.connect(self.print)
        dialog.exec_()

    def find(self, backwards=False):
        options = QTextDocument.FindFlags()
        if self.searchCaseSensitive.isChecked():
            options |= QTextDocument.FindCaseSensitively
        if backwards:
            options |= QTextDocument.FindBackward
        if not self.editor.find(self.searchLine.text(), options):
            self.searchLine.setStyleSheet('QLineEdit {background: yellow}')
        else:
            self.searchLine.setStyleSheet('')

    def toggleSearchDock(self):
        self.searchDock.setVisible(not self.searchDock.isVisible())
        if self.searchDock.isVisible():
            self.searchLine.setFocus(True)

    def showEvent(self, event):
        QMainWindow.showEvent(self, event)
        # work around QTBUG-16507
        filepath = self.windowFilePath()
        self.setWindowFilePath(filepath+'x')
        self.setWindowFilePath(filepath)

    def closeEvent(self, event):
        if not self.askSaveChanges():
            event.ignore()
        else:
            self.saveSettings()
            QMainWindow.closeEvent(self, event)

    def about(self):
        app = QApplication.instance()
        args = {'name': app.applicationName(),
                'version': app.applicationVersion()}
        title = self.trUtf8(b'{name} {version}').format(**args)
        text = self.trUtf8("""\
<h1>{name} {version}</h1>

<p>An trivial text editor implemented in Qt</p>

<p>Copyright © 2011 <a href="mailto:lunaryorn@googlemail.com">Sebastian
Wiesner</a></p>

<p>Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:<p>

<ul><li>The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.</li></ul>

<p><strong>The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.</strong></p>""").format(**args)
        QMessageBox.about(self, title, text)


class TextEditorApplication(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.setApplicationName('Text editor')
        self.setOrganizationName('lunaryorn')
        self.setOrganizationDomain('lunaryorn.de')
        self.setApplicationVersion(__version__)


def main():
    app = TextEditorApplication(sys.argv)
    arguments = app.arguments()
    editor = TextEditor()
    editor.show()
    if len(arguments) > 1:
        editor.load(arguments[1])
    app.exec_()


if __name__ == '__main__':
    main()
