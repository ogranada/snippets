# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""
    dbus_glib_hal_signals
    =====================

    Demonstrate the use of dbus to react to HAL events.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""

from __future__ import print_function, division

from functools import partial

import dbus
from glib import MainLoop
from dbus.mainloop.glib import DBusGMainLoop

# use glib as dbus main loop
DBusGMainLoop(set_as_default=True)

HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MANAGER_PATH = '/org/freedesktop/Hal/Manager'
HAL_MANAGER_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEVICE_IFACE = 'org.freedesktop.Hal.Device'


def device_added(bus, udi):
    """
    Signal handler for the `DeviceAdded` signal of hal.

    ``bus`` is the bus connection, ``udi`` the universal device id of the
    new device.
    """
    # get the dbus object for the new device
    device = dbus.Interface(bus.get_object(HAL_SERVICE, udi),
                            HAL_DEVICE_IFACE)
    print('device with id {0} connected.'.format(udi))
    # check capabilities, only volumes on block devices are handled
    if device.QueryCapability('volume') and device.QueryCapability('block'):
        print('\tThe device is a storage volume.')
        # print the product name, if the device has one
        if device.PropertyExists('info.product'):
            name = device.GetPropertyString('info.product')
            print('\tProduct name: {0}'.format(name))
        else:
            print('\tThe device has no name')


def main():
    # connect to the system bus, which provides system services like HAL or
    # NetworkManager.  The session bus houses per-user applications like
    # media players
    bus = dbus.SystemBus()
    # get the hal manager object on this bus.  This object maintains a list
    # of devices and notifies clients about changes
    manager = dbus.Interface(bus.get_object(HAL_SERVICE, HAL_MANAGER_PATH),
                             HAL_MANAGER_IFACE)
    # connect to the signal, the bus is passed as "closure"
    manager.connect_to_signal('DeviceAdded', partial(device_added, bus))
    # start looping to handle incoming signals
    mainloop = MainLoop()
    mainloop.run()


if __name__ == '__main__':
    main()
