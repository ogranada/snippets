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
    A simple Qt4 socket example
    ===========================

    This snippet demonstrates the usage of the TCP socket classes of the
    QtNetwork module.

    If started with ``-s`` or ``--server`` option, a new server is spawned,
    which listens on 127.0.0.1:18888.  This server prints all received text
    onto standard output.  To shutdown the server, send the string
    ``'quit'`` to the server, for instance by using ``netcat``::

       echo 'quit' | nc localhost 18888

    If ``-s`` is not given, a graphical client is started.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
from functools import partial
from optparse import OptionParser

from PySide.QtCore import Signal, QObject, QTextStream, QTextCodec
from PySide.QtGui import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                         QLineEdit, QPlainTextEdit, QAction, QStyle)
from PySide.QtNetwork import QTcpSocket, QTcpServer, QHostAddress


HOST_ADDRESS = QHostAddress(QHostAddress.LocalHost)
PORT = 18888

def _stream_for_connection(connection):
    """
    Create a UTF_8 encoded text stream from the given ``connection``.
    """
    stream = QTextStream(connection)
    stream.setCodec(QTextCodec.codecForName(b'utf-8'))
    return stream


class ChatServer(QTcpServer):
    """
    Provide a simple plain text chat server.

    The chat server will await incoming connections and forward text send by
    a single client to all other clients (including the originating client).
    The server will terminate, if it receives the string ``'quit'``, case
    being ignored.
    """

    #: emitted if the server shuts down
    serverShutdown = Signal()
    #: emitted if the server receives text.  The text is given as argument
    #to slots
    textReceived = Signal(str)

    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)
        # all currently connected clients
        self.connections = set()
        # handle new clients
        self.newConnection.connect(self._handle_incoming_connection)

    def _handle_incoming_connection(self):
        # get a socket for this newly incoming connection
        connection = self.nextPendingConnection()
        # delete the connection upon disconnect
        connection.disconnected.connect(self._handle_disconnect)
        # remove any deleted connection from our list of connections
        connection.destroyed[QObject].connect(self.connections.remove)
        # handle data incoming from this client
        connection.readyRead.connect(self._handle_incoming_data)
        self.connections.add(connection)

    def _handle_disconnect(self):
        # delete our connection handle, if the client disconnects
        connection = self.sender()
        connection.deleteLater()

    def _handle_incoming_data(self):
        # read all data from the client
        connection = self.sender()
        text = _stream_for_connection(connection).readAll().strip()
        self.textReceived.emit(text)
        if text.lower() == 'quit':
            # shut the server down
            self.shutdown()
            return
        for connection in self.connections:
            stream = _stream_for_connection(connection)
            stream << text << '\n'

    def shutdown(self):
        """
        Shut the chat server down.
        """
        # remove all connections
        for connection in self.connections:
            connection.disconnectFromHost()
        # and tell anyone who cares, that we shutdown now
        self.serverShutdown.emit()


class ChatWidget(QWidget):
    """
    A chatting widget.
    """

    #: A notification (not chat!) message for the user
    message = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout(self))
        self.text_display = QPlainTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout().addWidget(self.text_display)
        self.text_input = QLineEdit(self)
        self.text_input.returnPressed.connect(self.send_text)
        self.layout().addWidget(self.text_input)
        QWidget.setTabOrder(self.text_input, self.text_display)
        self.setEnabled(False)
        self.message.emit('Not connected')
        self._connection = None

    @property
    def connected(self):
        """
        ``True``, if this chat widget is connected to some server, ``False``
        otherwise
        """
        return (self._connection and
                self._connection.state() == QTcpSocket.ConnectedState)

    @property
    def connection(self):
        """
        The connection used by this widget.
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection
        if not self.connected:
            # wait for connection, if the connection isn't available yet
            self._connection.connected.connect(self._enable_chat)
        else:
            self._enable_chat()
        # handle errors, disconnects and incoming data
        self._connection.error.connect(self._handle_error)
        self._connection.disconnected.connect(self._handle_disconnect)
        self._connection.readyRead.connect(self._receive_text)

    def _enable_chat(self):
        """
        Enable the chat widget for chatting.
        """
        self.message.emit('connected')
        self.setEnabled(True)
        # remove all text from the previous connection
        self.text_display.clear()

    def _handle_disconnect(self):
        """
        Handle a disconnect.
        """
        self.message.emit('disconnected')
        # disable the user interface
        self.setEnabled(False)
        # and disconnect from all slots and eventually delete the connection
        # itself
        self._connection.readyRead.disconnect(self._receive_text)
        self._connection.deleteLater()
        self._connection = None

    def _handle_error(self):
        self.message.emit(self._connection.errorString())

    def _receive_text(self):
        text = _stream_for_connection(self.connection).readAll()
        self.text_display.insertPlainText('{0}'.format(text))

    def send_text(self, text=None):
        """
        Send ``text`` over the connection of this widget.  Does nothing, if
        the widget is not connected.

        If ``text`` is ``None`` (the default), use the current input form
        the user.
        """
        if self.connected:
            stream = _stream_for_connection(self.connection)
            if not text:
                text = self.text_input.text()
                self.text_input.clear()
            stream << text


class ChatWindow(QMainWindow):
    """
    The chat application window.
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.chat_widget = ChatWidget(self)
        self.setCentralWidget(self.chat_widget)
        # set up all actions
        self.chat_widget.message.connect(self.statusBar().showMessage)
        app_menu = self.menuBar().addMenu('&Application')
        self.connect_action = QAction('&Connect', self)
        self.connect_action.triggered.connect(self._connect)
        self.connect_action.setShortcut('Ctrl+C')
        app_menu.addAction(self.connect_action)
        app_menu.addSeparator()
        self.quit_server_action = QAction('Quit &server', self)
        self.quit_server_action.triggered.connect(self._quit_server)
        self.quit_server_action.setEnabled(False)
        self.quit_server_action.setShortcut('Ctrl+D')
        app_menu.addAction(self.quit_server_action)
        quit_action = QAction(self.style().standardIcon(
            QStyle.SP_DialogCloseButton), '&Quit', self)
        quit_action.triggered.connect(QApplication.instance().quit)
        quit_action.setShortcut('Ctrl+Q')
        app_menu.addAction(quit_action)
        # attempt to connect
        self._connect()

    def _quit_server(self):
        if self.chat_widget.connected:
            self.chat_widget.send_text('quit')

    def _connect(self):
        # connect to a server
        if not self.chat_widget.connected:
            self.chat_widget.connection = QTcpSocket()
            # upon connection, disable the connect action, and enable the
            # quit server action
            self.chat_widget.connection.connected.connect(
                partial(self.quit_server_action.setEnabled, True))
            self.chat_widget.connection.connected.connect(
                partial(self.connect_action.setDisabled, True))
            # to the reverse thing upon disconnection
            self.chat_widget.connection.disconnected.connect(
                partial(self.connect_action.setEnabled, True))
            self.chat_widget.connection.disconnected.connect(
                partial(self.quit_server_action.setDisabled, True))
            # connect to the chat server
            self.chat_widget.connection.connectToHost(HOST_ADDRESS, PORT)


def main():
    parser = OptionParser(
        description='A chat client/server')
    parser.add_option('-s', '--server', help='Start a server.  If not '
                      'given, a client will be started',
                      action='store_true')
    opts, args = parser.parse_args()
    if opts.server:
        from PySide.QtCore import QCoreApplication
        app = QCoreApplication(sys.argv)
        # spawn a server
        server = ChatServer()
        listening = server.listen(HOST_ADDRESS, PORT)
        if not listening:
            # a server error
            print('Server start failed: {}'.format(server.errorString()),
                  file=sys.stderr)
        server.serverShutdown.connect(app.quit)
        # print everything received by the server to standard output
        server.textReceived.connect(partial(print, '>>'))
    else:
        app = QApplication(sys.argv)
        chat_window = ChatWindow()
        chat_window.show()

    app.exec_()



if __name__ == '__main__':
    main()
