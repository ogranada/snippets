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
    A fully-featured Qt4 model class using XML for data storage (through
    lxml).  The xml looks like the following::

        <stringlist>
          <string caption="foo" />
          <string caption="bar">
            <string caption="spam">
              <string caption="eggs" />
            </string>
          </string>
        </stringlist>

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

from itertools import count
from copy import deepcopy

from lxml import etree
from PySide.QtCore import Qt, QAbstractItemModel, QModelIndex, QMimeData


class AnalysisModel(QAbstractItemModel):
    """A hierarchical model, containing strings."""

    def __init__(self, filename, parent=None):
        """
        Creates a new AnalysisModel.  ``filename`` is a xml file, containing
        the strings to display.
        """
        QAbstractItemModel.__init__(self, parent)
        self.filename = filename
        self.strings = etree.parse(self.filename)
        # assign initial id for xml root item (``stringlist``)
        self.strings.getroot().set('id', '0')
        # increasing counter to auto-assign ids
        # initial counter value is the maximum of all ids, that were already
        # stored inside the xml file.  This avoids double-assignment of ids.
        self.all_ids_in_tree = etree.XPath('//*/attribute::id')
        ids = map(int, self.all_ids_in_tree(self.strings))
        initial = max(ids) + 1
        self.id_counter = count(initial)
        # a xpath selector to find an element with a specific id
        self.select_by_id = etree.XPath('//*[@id=$id]')
        # find all elements, that have id attributes
        self.select_elements_with_id = etree.XPath('//*[@id]')

    def _get_element_by_id(self, id):
        """
        Returns the xml element for ``id``.

        :raises IndexError:  If ``id`` does not exist in the xml tree
        """
        return self.select_by_id(self.strings, id=id)[0]

    def _get_element_for_index(self, index):
        """Returns the lxml etree element for model ``index``."""
        return self._get_element_by_id(index.internalId())

    def _remove_elements_by_ids(self, ids):
        """Removes all elements corresponding to ``ids`` from this model."""
        for id in ids:
            try:
                el = self._get_element_by_id(id)
            except IndexError:
                continue
            else:
                row = el.getparent().index(el)
                index = self.createIndex(row, 0, int(id))
                self.removeRow(index.row(), index.parent())

    def _insert_element(self, row, element, parent):
        """Inserts an etree element into this model."""
        self.insertRow(row, parent)
        index = self.index(row, 0, parent)
        self.setData(index, element.get('caption'))
        for subelement in element:
            self._insert_element(self.rowCount(index), subelement, index)

    def index(self, row, column, parent=QModelIndex()):
        """
        Creates a model index for element at ``row`` and ``column``.

        ``parent`` is the parent model index.  If it is invalid, it refers
        to the model's root index.
        """
        if column != 0:
            # we only support one column, all others lead to invalid indexes
            return QModelIndex()
        try:
            el = self._get_element_for_index(parent)[row]
            if not 'id' in el.attrib:
                # assign an id, if the element doesn't have one yet
                el.set('id',  str(self.id_counter.next()))
            # create the index, and associate it with the etree element
            # using the element's id as internal id for the new index
            return self.createIndex(row,  column,  int(el.get('id')))
        except IndexError:
            return QModelIndex()

    def parent(self, index):
        """Returns the parent model index of ``index``."""
        if index.isValid():
            element = self._get_element_for_index(index)
            # retrieve the parent element of the current one
            # (element -> strings -> parent string)
            parent = element.getparent()
            # check the tag name (it could also be the root stringlist item,
            # in which case the invalid fall back index must be returned)
            if parent.tag == 'string':
                # assign id if necessary
                if not 'id' in parent.attrib:
                    parent.set('id',  str(self.id_counter.next()))
                # determine the index of the parent element inside its
                # container.  This index is the "row" of the parent element
                row = parent.getparent().index(parent)
                return self.createIndex(row, 0, int(parent.get('id')))
        # return invalid model index as fallback
        return QModelIndex()

    def flags(self, index):
        """Returns supported actions for ``index``."""
        return (Qt.ItemIsEditable | Qt.ItemIsEnabled |
                Qt.ItemIsSelectable | Qt.ItemIsDragEnabled |
                Qt.ItemIsDropEnabled)

    def supportedDropActions(self):
        """Returns the drag n' drop actions supported by this model."""
        return Qt.CopyAction | Qt.MoveAction

    def mimeTypes(self):
        """
        Returns a list of mimetypes supported by this model for dropping.
        """
        return ['text/xml']

    def mimeData(self, indexes):
        """Encodes ``indexes`` as mime data for dragging."""
        # serialize data as xml
        root = etree.Element('stringlist')
        for index in indexes:
            element = self._get_element_for_index(index)
            root.append(deepcopy(element))
        serialized = etree.tostring(root, xml_declaration=True)
        mimedata = QMimeData()
        mimedata.setData('text/xml', serialized)
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        """
        Drops mime ``data`` under ``parent`` item, at ``row`` and
        ``column``.  ``action`` is the action to be performed.
        """
        if action == Qt.IgnoreAction:
            return False
        if column > 0:
            return False
        # de-serialize xml data
        serialized = str(data.data('text/xml'))
        root = etree.fromstring(serialized)
        # remove old element, if items are moved within the tree
        if action == Qt.MoveAction:
            ids = self.all_ids_in_tree(root)
            self._remove_elements_by_ids(ids)
        # insert the new items
        if row == -1:
            row = self.rowCount(parent)
        for element in root:
            self._insert_element(row, element, parent)
        return True

    def setData(self, index, value, role=Qt.EditRole):
        """
        Sets the item at ``index`` to ``value``.
        Return ``True``, if successful, otherwise ``False``.
        """
        if not index.isValid() or role != Qt.EditRole:
            return False
        element = self._get_element_for_index(index)
        data = unicode(value.toString())
        element.set('caption', data)
        self.dataChanged.emit(index, index)
        return True

    def data(self, index, role=Qt.DisplayRole):
        """Returns the data at ``index``."""
        # index must be valid and we must be in display role
        if index.isValid() and role == Qt.DisplayRole:
            # return the caption of the element associated with
            # ``index``
            element = self._get_element_for_index(index)
            return element.get('caption')
        else:
            # return nothing to indicate invalid values
            return

    def insertRows(self, position, rows, parent=QModelIndex()):
        """Inserts rows into this model."""
        parent_el = self._get_element_for_index(parent)
        self.beginInsertRows(parent, position, position+rows-1)
        # create the container element, if necessary
        # insert necessary elements
        for i in xrange(rows):
            el = etree.Element(
                'string', id= str(self.id_counter.next()))
            parent_el.insert(position, el)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent):
        "Remove rows from model."
        parent_el = self._get_element_for_index(parent)
        # tell the view, that we're manipluating the internal data structure
        self.beginRemoveRows(parent, position, position+rows-1)
        for i in xrange(rows):
            del parent_el[position]
        self.endRemoveRows()
        return True

    def rowCount(self,  parent):
        """
        Returns the number of child elements under ``parent``.  An
        invalid index as parent refers to the root element.
        """
        return len(self._get_element_for_index(parent))

    def columnCount(self,  parent):
        """
        Returns number of columns under ``parent`` index.  This method
        always returns ``1``, because this model doesn't have multiple
        columns.
        """
        return 1

    def submit(self):
        """
        Writes internal data structure to disk.

        :raises EnvironmentError:  On write errors
        """
        self.strings.write(self.filename, encoding='utf-8',
                           xml_declaration=True, pretty_print=True)
        return True
