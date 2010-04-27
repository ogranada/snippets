#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2008, 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    A simple Qt4 socket example
    ===========================

    This snippet demonstrates the usage of the TCP socket classes of the
    QtNetwork module.

    If started with ``-s`` or ``--server`` option, a new server is spawn,
    which listens on 127.0.0.1:18888.

    If started with ``-c`` or ``--client`` option, a little client shell is
    spawn.  It requires a running server.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import with_statement

import sys
import textwrap
from getopt import getopt
from contextlib import closing

from PyQt4 import QtCore, QtGui, QtNetwork


HOST_ADDRESS = QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost)
PORT = 18888


class QSocketTestMainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Qt4 socket example')
        # use QTextEdit in read only mode together with a document cursor to
        # display incoming text.  In Qt 4.4 QPlainTextEdit could be used,
        # which would simplify text handling.
        self.text_display = QtGui.QTextEdit(self)
        self.text_display.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.text_display.setReadOnly(True)
        self.setCentralWidget(self.text_display)
        self.document_cursor = QtGui.QTextCursor(
            self.text_display.document())
        # server to listen for incoming connections
        self.server = QtNetwork.QTcpServer(self)
        self.connect(self.server, QtCore.SIGNAL('newConnection()'),
                     self.handle_connection)
        # connections
        self.connections = set()

    def handle_connection(self):
        """Called, if a new client connects."""
        # handle all incoming connections
        while self.server.hasPendingConnections():
            connection = self.server.nextPendingConnection()
            # destroy the sockets if gots disconnected
            self.connect(connection, QtCore.SIGNAL('disconnected()'),
                         connection, QtCore.SLOT('deleteLater()'))
            # remove the socket from the internal list of connections, if it
            # is destroyed
            self.connect(connection, QtCore.SIGNAL('destroyed(QObject *)'),
                         self.remove_connection)
            # connect handler for incoming data
            self.connect(connection, QtCore.SIGNAL('readyRead()'),
                         self.read_data)
            self.connections.add(connection)

    def remove_connection(self, connection):
        """Remove `connection` from the internal connection list."""
        self.connections.remove(connection)

    def read_data(self):
        """Called to read data."""
        # create a stream with proper encoding.  This gives us a QString
        # instance directly without any conversion between Pythons builtins
        # and QString
        stream = QtCore.QTextStream(self.sender())
        stream.setCodec(QtCore.QTextCodec.codecForName('utf-8'))
        # move the the end of the document of the display widget
        self.document_cursor.movePosition(QtGui.QTextCursor.End)
        # and insert text with a final new line
        self.document_cursor.insertText(stream.readAll())
        self.document_cursor.insertText('\n')

    def showEvent(self, evt):
        if not self.server.isListening():
            # start listening, if the main window is shown
            listening = self.server.listen(HOST_ADDRESS, PORT)
            if not listening:
                QtGui.QMessageBox.critical(self, 'Server start failed',
                                           self.server.errorString())
        evt.accept()

    def closeEvent(self, evt):
        # close all connections and the server
        for connection in self.connections:
            connection.close()
        self.server.close()
        evt.accept()


def start_server():
    app = QtGui.QApplication(sys.argv)
    QSocketTestMainWindow().show()
    app.exec_()


def start_client():
    with closing(QtNetwork.QTcpSocket()) as socket:
        socket.connectToHost(HOST_ADDRESS, PORT, QtCore.QIODevice.WriteOnly)
        # wait five seconds for connection
        connected = socket.waitForConnected(5000)
        if not connected:
            # if connection failed, print error and exit
            print socket.errorString()
            return
        while socket.state() == QtNetwork.QTcpSocket.ConnectedState:
            # request input, as long as the socket is connected
            try:
                inp = raw_input('Enter a string (Strg+D, Strg+C to quit): ')
                # decode input and send it utf-8-encoded to the server
                socket.write(inp.decode(sys.stdin.encoding).encode('utf-8'))
                # flush to make data appear at the server immediatly
                socket.flush()
            except (KeyboardInterrupt, EOFError):
                print '\nGoing peacefully'
                # exit
                return


def main():
    optlist, args = getopt(sys.argv[1:], 'sch',
                           ['server', 'client', 'help'])
    if args:
        sys.exit('This program does not unterstand arguments')
    # parse options
    client = server = False
    for opt, arg in optlist:
        if opt in ('-h', '--help'):
            # print help and exit
            print textwrap.dedent(__doc__)
            return
        elif opt in ('-c', '--client'):
            client = True
        elif opt in ('-s', '--server'):
            server = True

    if client and server:
        print 'Cannot run in client and server mode.'
        print 'Please choose one mode!'

    if client:
        start_client()
    elif server:
        start_server()
    else:
        print textwrap.dedent(__doc__)


if __name__ == '__main__':
    main()
