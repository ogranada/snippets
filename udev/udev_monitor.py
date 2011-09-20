#!/usr/bin/env python2
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
    Monitor mouse devices with udev.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
from signal import signal, SIGINT
from functools import partial

from pyudev import Context, Monitor
from pyudev.pyside import QUDevMonitorObserver
from PySide.QtCore import QCoreApplication


def print_mouse_status(device, status_message):
    try:
        is_mouse = device.asbool('ID_INPUT_MOUSE')
    except KeyError:
        pass
    else:
        if is_mouse and device.sys_name.startswith('event'):
            name = device.parent['NAME']
            print(name, status_message)


def main():
    app = QCoreApplication(sys.argv)
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='input')
    observer = QUDevMonitorObserver(monitor)
    observer.deviceAdded.connect(
        partial(print_mouse_status, status_message="added"))
    observer.deviceRemoved.connect(
        partial(print_mouse_status, status_message="removed"))
    monitor.start()

    app.exec_()


if __name__ == '__main__':
    main()

