#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

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
    hal_touchpad_daemon
    ===================

    Disables a synpatics touchpad, if an external mouse is
    plugged in.

    This script forks into background automatically.  Use the DBus interface
    to kill it::

       dbus-send --session --dest='de.lunaryorn.TouchpadDaemon' --type=method_call /de/lunaryorn/TouchpadDaemon de.lunaryorn.TouchpadDaemon.Quit

    or simplier::

       qdbus --session de.lunaryorn.TouchpadDaemon /de/lunaryorn/TouchpadDaemon de.lunaryorn.TouchpadDaemon.Quit


    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import os
import sys
import shlex
import subprocess
from functools import partial

import dbus
import gobject
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


ICON = '/path/to/icon'


class MouseListener(dbus.service.Object):
    def __init__(self):
        self.bus = dbus.SystemBus()
        self._get_hal_object = partial(self.bus.get_object,
                                       'org.freedesktop.Hal')
        self.manager = dbus.Interface(
            self._get_hal_object('/org/freedesktop/Hal/Manager'),
            dbus_interface='org.freedesktop.Hal.Manager')
        self._plugged_mouse_devices = set()
        self._find_mouse_devices()
        manager_signal = partial(
            self.bus.add_signal_receiver,
            dbus_interface='org.freedesktop.Hal.Manager')
        manager_signal(self._device_added, 'DeviceAdded')
        manager_signal(self._device_removed, 'DeviceRemoved')

    def _find_mouse_devices(self):
        for udi in self.manager.FindDeviceByCapability('input.mouse'):
            self._register_mouse_device(udi)

    def _get_device_object(self, udi):
        return dbus.Interface(self._get_hal_object(udi),
                              dbus_interface='org.freedesktop.Hal.Device')

    def _register_mouse_device(self, udi):
        device = self._get_device_object(udi)
        if device.QueryCapability('input.mouse'):
            self._plugged_mouse_devices.add(udi)
            return True

    def _unregister_mouse_device(self, udi):
        if udi in self._plugged_mouse_devices:
            self._plugged_mouse_devices.remove(udi)
            return True

    def _device_removed(self, udi):
        if self._unregister_mouse_device(udi):
            subprocess.call(['synclient', 'TouchpadOff=0'])
            self.notify(u'Touchpad', u'Touchpad eingeschaltet')

    def _device_added(self, udi):
        if self._register_mouse_device(udi):
            subprocess.call(['synclient', 'TouchpadOff=1'])
            self.notify(u'Touchpad', u'Touchpad ausgeschaltet')

    def notify(self, title, message):
        enc = sys.getfilesystemencoding()
        subprocess.call(['/usr/bin/notify-send', '-i', ICON,
                         title.encode(enc), message.encode(enc)])


class MainLoopDbusObject(dbus.service.Object):
    def __init__(self,wrapped, *args, **kwargs):
        dbus.service.Object.__init__(self, *args, **kwargs)
        self.wrapped = wrapped

    @dbus.service.method(dbus_interface='de.lunaryorn.TouchpadDaemon',
                         in_signature='', out_signature='')
    def Quit(self):
        self.wrapped.quit()


def main():
    # fork into backgroud
    if os.fork() == 0:
        os.setsid()
        if os.fork() == 0:
            os.chdir('/')
            os.umask(0)
        else:
            os._exit(0)
    else:
        os._exit(0)

    # run mainloop
    loop = gobject.MainLoop()
    # register loop
    bus_name = dbus.service.BusName('de.lunaryorn.TouchpadDaemon',
                                    bus=dbus.SessionBus())
    bus_object = MainLoopDbusObject(
        loop, object_path='/de/lunaryorn/TouchpadDaemon',
        bus_name=bus_name)
    # setup listener
    listener = MouseListener()
    loop.run()


if __name__ == '__main__':
    main()
