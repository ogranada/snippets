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

"""
    A customized QTreeWidget which provides foldable check boxes.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

from PySide.QtCore import Qt
from PySide.QtGui import (QApplication, QMainWindow, QGroupBox, QTreeWidget,
                          QTreeWidgetItem, QVBoxLayout, QFrame, QPalette)

GROUPS = [
    ('first_group', 'First group', [
        ('first_choice', 'First choice'),
        ('second_choice', 'Second choice')
    ]),
    ('second_group', 'Second group', [
        ('third_choice', 'Third choice')
    ])
]


class FoldableCheckBoxes(QTreeWidget):

    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)
        # the following makes this treeview look like a collection of
        # checkboxes and labels, and not like a tree view.
        # use the standard window background
        self.viewport().setBackgroundRole(QPalette.Window)
        # no border
        self.setFrameShape(QFrame.NoFrame)
        # disable selections to hide the selection shadow when moving the mouse
        # over items.  Selection isn't needed anyways, because we are just
        # interested in checking and unchecking items
        self.setSelectionMode(QTreeWidget.NoSelection)
        # disable focus for the whole widget.  This avoids focus lines around
        # items when checking or unchecking items.  Since the items aren't
        # editable, we don't need focus anyways.
        self.setFocusPolicy(Qt.NoFocus)
        # hide the header
        self.setHeaderHidden(True)

        # the following mappings store groups and options
        self._groups = {}
        self._options = {}

    def addGroup(self, name, title):
        """
        Add a new group.

        ``name`` and ``title`` are unicode strings.  ``name`` is used to
        identify this group, ``title`` is displayed to the user.
        """
        if name in self._groups:
            raise ValueError('Duplicate group')
        self._groups[name] = QTreeWidgetItem([title])
        self.addTopLevelItem(self._groups[name])
        # expand groups initially
        self.setGroupExpanded(name, True)

    def addOption(self, group_name, name, title):
        """
        Add an option to a group.

        All arguments are unicode strings. ``group_name`` is the name of the
        group this option is added to.  ``name`` is the name of the option
        itself, ``title`` is displayed to the user.
        """
        if name in self._options:
            raise ValueError('Duplicate option')
        group_item = self._groups[group_name]
        self._options[name] = QTreeWidgetItem(group_item, [title])
        # uncheck options initially
        self.setOptionChecked(name, False)

    def isOptionChecked(self, option):
        """
        Return ``True``, if the given ``option`` is checked, ``False``
        otherwise.

        ``option`` is a unicode string containing an option name.
        """
        return self._options[option].checkState(0) == Qt.Checked

    def setOptionChecked(self, option, checked):
        """
        Check or uncheck the given ``option``.

        If ``checked`` is ``True``, the option is checked, otherwise it is
        unchecked.

        ``option`` is an option name as unicode string.  ``checked`` is a
        boolean.
        """
        state = Qt.Checked if checked else Qt.Unchecked
        self._options[option].setCheckState(0, state)

    def isGroupExpanded(self, group):
        """
        Return ``True``, if the given ``group`` is expanded, ``False``
        otherwise.

        ``group`` is the group name as unicode string.
        """
        return self._groups[group].isExpanded()

    def setGroupExpanded(self, group, expanded):
        """
        Expand or collapse the given ``group``.

        If ``expanded`` is ``True``, the group is expanded, otherwise it is
        collapsed.

        ``group`` is the group name as unicode string. ``expanded`` is a
        boolean.
        """
        self._groups[group].setExpanded(expanded)


def main():
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    group = QGroupBox('Some options', mainwindow)
    group.setLayout(QVBoxLayout(group))
    mainwindow.setCentralWidget(group)
    boxes = FoldableCheckBoxes(group)
    for group_name, title, items in GROUPS:
        boxes.addGroup(group_name, title)
        for name, title in items:
            boxes.addOption(group_name, name, title)
    group.layout().addWidget(boxes)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
