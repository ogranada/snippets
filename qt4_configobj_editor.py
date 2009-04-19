#!/usr/bin/python
# Copyright (c) 2008, 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

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
    config_editor
    =============

    A PoC-Widget which provides an interface to edit configobj sections.

    :author: Sebastian Wiesner
    :contact: basti.wiesner@gmx.net
    :copyright: 2008 by Sebastian Wiesner
    :license: MIT
"""

import sys
from collections import defaultdict

import validate
from configobj import ConfigObj
from PyQt4 import QtCore, QtGui

# indicates a missing default value
NoDefault = type('NoDefault', (object,),
                 {'__nonzero__': lambda self: False,
                  '__str__': lambda self: ''})()


class QCheckBoxWrapper(QtGui.QCheckBox):
    def init_widget(self, *args, **kwargs):
        self.setChecked(bool(self.default_value))
    def _get_config_value(self):
        return self.isChecked()
    def _set_config_value(self, value):
        self.setChecked(bool(value))
    config_value = property(_get_config_value, _set_config_value)

class QLineEditWrapper(QtGui.QLineEdit):
    def init_widget(self, *args, **kwargs):
        self.setText(self.default_value or '')
    def _get_config_value(self):
        value = unicode(self.text()) or self.default_value
        return value
    def _set_config_value(self, value):
        default = self.default_value or ''
        self.setText(value or default)
    config_value = property(_get_config_value, _set_config_value)

class QComboBoxWrapper(QtGui.QComboBox):
    def init_widget(self, *args, **kwargs):
        self.insertItems(0, list(args))
        if self.default_value is not NoDefault:
            self.setCurrentIndex(self.findText(self.default_value))
    def _get_config_value(self):
        return unicode(self.currentText())
    def _set_config_value(self, value):
        self.setCurrentIndex(self.findText(value))
    config_value = property(_get_config_value, _set_config_value)

class QSpinBoxWrapper(QtGui.QSpinBox):
    def init_widget(self, *args, **kwargs):
        min = -sys.maxint
        max = sys.maxint
        if args:
            min, max = map(int, args)
        if kwargs:
            min = int(kwargs['min'])
            max = int(kwargs['max'])
        self.setRange(min, max)
        self.setValue(self.default_value or 0)
    def _get_config_value(self):
        return self.value()
    def _set_config_value(self, value):
        self.setValue(value)
    config_value = property(_get_config_value, _set_config_value)

class QDoubleSpinBoxWrapper(QtGui.QDoubleSpinBox):
    def init_widget(self, *args, **kwargs):
        if args:
            self.setRange(*map(float, args))
        if kwargs:
            self.setRange(float(kwargs['min']), float(kwargs['max']))
        self.setValue(self.default_value or 0)
    def _get_config_value(self):
        return self.value()
    def _set_config_value(self, value):
        self.setValue(value)
    config_value = property(_get_config_value, _set_config_value)


class SectionEditor(QtGui.QWidget):
    """
    A dialog, which provides a simple interface to edit a config section.

    The :attr:`check_widgets` attribute maps the name of a config check to a
    widget class.  This widget class must have a ``config_value`` property.
    It gets a ``default_value`` attribute, that represents the default
    value.  The attribute may be the special ``NoDefault`` to indicate, that
    this widget doesn't have a default value.

    Additionally, this widget must have a ``init_widget`` method, which
    receives ``*args`` and ``**kwargs`` as specified in the config check.
    Inside this method, the widget should initialize itself and set the
    default value.

    :cvar check_widgets:  Widgets associated to check names
    """

    check_widgets = defaultdict(
        lambda: QLineEditWrapper,
        boolean=QCheckBoxWrapper,
        option=QComboBoxWrapper,
        integer=QSpinBoxWrapper,
        float=QDoubleSpinBoxWrapper)

    def __init__(self, section, check_funcs=None, parent=None):
        """
        Create a new edit widget.

        :param section: The section to edit
        :param parent: The parent widget
        :param check_funcs:  Additional validation functions to pass to the
                             validator
        """
        QtGui.QWidget.__init__(self, parent)
        self.section = section
        self.validator = validate.Validator(check_funcs)
        if not section.configspec:
            raise ValueError('%r has no configspec' % section)
        self.setup_ui()

    def setup_ui(self):
        self.dialog_layout = QtGui.QVBoxLayout(self)
        self.section_layout = QtGui.QGridLayout()
        for row, key in enumerate(self.section.configspec):
            label = QtGui.QLabel(key, self)
            self.section_layout.addWidget(label, row, 0)
            widget = self.create_widget(key)
            self.section_layout.addWidget(widget, row, 1)
        self.dialog_layout.addLayout(self.section_layout)
        self.dialog_layout.addStretch()
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Apply,
            QtCore.Qt.Horizontal, self)
        self.dialog_layout.addWidget(self.buttons)
        self.connect(self.buttons,
                     QtCore.SIGNAL('clicked(QAbstractButton *)'),
                     self.button_clicked)

    def create_widget(self, key):
        """
        Create a widget fo ``key``.
        """
        typename, args, kwargs, default = self.validator._parse_with_caching(
            self.section.configspec[key])
        widget = self.check_widgets[typename](self)
        widget.setObjectName(key)
        try:
            widget.default_value = self.validator.get_default_value(
                self.section.configspec[key])
        except KeyError:
            widget.default_value = NoDefault
        widget.init_widget(*args, **kwargs)
        try:
            if key in self.section:
                widget.config_value = self._check_value(key,
                                                        self.section[key])
        except (validate.VdtTypeError, validate.VdtValueError):
            pass
        return widget

    def button_clicked(self, button):
        """
        Called to handle a click on ``button``.

        :type button: QtGui.QAbstractButton
        """
        ok = self.buttons.button(QtGui.QDialogButtonBox.Ok)
        cancel = self.buttons.button(QtGui.QDialogButtonBox.Cancel)
        apply = self.buttons.button(QtGui.QDialogButtonBox.Apply)
        errormsg_tmpl = ('Invalid value for %s: %s\n'
                         'The value will not be saved.')
        if button is apply:
            for key in self.section.configspec:
                try:
                    self._save_key(key)
                except (validate.VdtTypeError, validate.VdtValueError), err:
                    QtGui.QMessageBox.warning(self, 'Invalid value',
                                              errormsg_tmpl % (key, err))
        elif button is ok:
            for key in self.section.configspec:
                try:
                    self._save_key(key)
                except (validate.VdtTypeError, validate.VdtValueError), err:
                    res = QtGui.QMessageBox.warning(
                        self, 'Invalid value', errormsg_tmpl % (key, err),
                        QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
                        QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Cancel:
                        # cancel the whole thing
                        return
        if button is cancel or button is ok:
            self.close()

    def _get_typename_of_key(self, key):
        """Returns the name of the type of ``key``."""
        check = self.section.configspec[key]
        name, args, _, default = self.validator._parse_with_caching(check)
        return name

    def _check_value(self, key, value):
        """
        Checks, if ``value`` has proper type for ``key`` and performs
        type conversion.  The converted value is returned.

        :raises validate.VdtTypeError: if ``value`` has invalid type
        :raises validate.VdtValueError: if ``value`` is invalid for ``key``
        """
        return self.validator.check(self.section.configspec[key], value)

    def _save_key(self, key):
        """Saves the widget value for ``key`` in the config obj."""
        typename = self._get_typename_of_key(key)
        cls = self.check_widgets[typename]
        widget = self.findChild(cls, key)
        value = widget.config_value
        if value != widget.default_value:
            # just for safety, we validate each value again
            self._check_value(key, value)
            self.section[key] = value


def main():
    app = QtGui.QApplication(sys.argv)
    spec = ConfigObj("""\
[foobar]
bool_key=boolean(default=False)
option_key=option(SPAM, EGGS, BAR, FOO, default=SPAM)
string_key=string(max=3,default=None)
int_key=integer(0, 100, default=10)
float_key=float(0, 100, default=10)
""".splitlines(), list_values=False)
    config = ConfigObj("""\
[foobar]
option_key=SPAM
string_key=spam
""".splitlines(), configspec=spec)
    dialog = SectionEditor(config['foobar'])
    dialog.show()
    app.exec_()
    print config

if __name__ == '__main__':
    main()
