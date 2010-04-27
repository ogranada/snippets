#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

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
    qt4_dbus_trayicon_app
    =====================

    A sample application, which uses a combination of DBus and a system tray
    icon, to keep a single instance running and allow remote control of this
    instance.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import sys

import dbus
import dbus.service
from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4 import QtGui, QtCore

# use the qt mainloop to handle dbus connections
DBusQtMainLoop(set_as_default=True)


class DBusTrayMainWindow(QtGui.QMainWindow):
    """A sample main window"""

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setup_gui()

    def setup_gui(self):
        """Sets up a sample gui interface."""
        central_widget = QtGui.QWidget(self)
        central_widget.setObjectName('central_widget')
        self.label = QtGui.QLabel('Hello World')
        self.input_field = QtGui.QLineEdit()
        change_button = QtGui.QPushButton('Change text')
        close_button = QtGui.QPushButton('close')
        quit_button = QtGui.QPushButton('quit')
        central_layout = QtGui.QVBoxLayout()
        button_layout = QtGui.QHBoxLayout()
        central_layout.addWidget(self.label)
        central_layout.addWidget(self.input_field)
        # a separate layout to display buttons horizontal
        button_layout.addWidget(change_button)
        button_layout.addWidget(close_button)
        button_layout.addWidget(quit_button)
        central_layout.addLayout(button_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        # create a system tray icon. Uncomment the second form, to have an
        # icon assigned, otherwise you will only be seeing an empty space in
        # system tray
        self.systemtrayicon = QtGui.QSystemTrayIcon(self)
        self.systemtrayicon.show()
        # set a fancy icon
        ## self.systemtrayicon.setIcon(QtGui.QIcon('/path/to/fancy/icon'))
        self.connect(change_button, QtCore.SIGNAL('clicked()'),
                     self.change_text)
        self.connect(quit_button, QtCore.SIGNAL('clicked()'),
                     QtGui.QApplication.instance().quit)
        self.connect(close_button, QtCore.SIGNAL('clicked()'),
                     self.hide)
        # show main window, if the system tray icon was clicked
        self.connect(
            self.systemtrayicon,
            QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'),
            self.icon_activated)

    def icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.setVisible(self.isHidden())

    def change_text(self):
        self.label.setText(self.input_field.text())

    def closeEvent(self, evt):
        # only hide, if the user requests a close
        evt.ignore()
        self.hide()


class DBusTrayMainWindowObject(dbus.service.Object):
    """DBus wrapper object for the mainwindow."""

    def __init__(self, mainwindow, bus):
        """Creates a new service object. `mainwindow` specifies the window,
        which is to be exposed through this service object. `bus` is the
        DBus bus, at which this object is registered."""
        # register this object on the given bus
        dbus.service.Object.__init__(self, bus,
                                     # the dbus object path
                                     '/lunar/PyQt4DBusTest/MainWindow')
        self.mainwindow = mainwindow

    # expose two methods on the lunar.PyQt4DBusTest.Window interface
    @dbus.service.method(dbus_interface='lunar.PyQt4DBusTest.Window')
    def show(self):
        self.mainwindow.show()

    @dbus.service.method(dbus_interface='lunar.PyQt4DBusTest.Window')
    def activateWindow(self):
        self.mainwindow.activateWindow()

def main():
    app = QtGui.QApplication(sys.argv)
    # connect to the current user's session bus
    bus = dbus.SessionBus()

    try:
        # try to connect to our service.  If this fails with a dbus
        # exception, the application is already running.
        mainwindow = bus.get_object('lunar.PyQt4DBusTest',
                                    '/lunar/PyQt4DBusTest/MainWindow')
    except dbus.DBusException:
        # the application is not running, so the service is registered and
        # the window created
        name = dbus.service.BusName('lunar.PyQt4DBusTest', bus)
        mainwindow = DBusTrayMainWindow()
        # register the service object for the main window
        mainwindowobject = DBusTrayMainWindowObject(mainwindow, bus)
        # show the window and get the message loop running
        mainwindow.show()
        app.exec_()
    else:
        # the try clause completed, the application must therefore be
        # running.  Now the mainwindow is shown and activated.
        mainwindow.show()
        mainwindow.activateWindow()


if __name__ == '__main__':
    main()
