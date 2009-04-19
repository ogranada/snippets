#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Uses the hal dbus api to obtain the serials of all storage devices
# Copyright (c) 2007, 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    hal_usage
    =========

    How to use Hal via DBus to retrieve a list of storage devices.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


import sys
import dbus


def list_devices(list_removable=False):
    # connect to the system bus
    bus = dbus.SystemBus()
    # a partial function to get objects from the hal service
    get_object = partial(bus.get_object, 'org.freedesktop.Hal')
    # get the manager object
    manager = dbus.Interface(
        get_object('/org/freedesktop/Hal/Manager'),
        dbus_interface='org.freedesktop.Hal.Manager')
    devices = manager.FindDeviceStringMatch('storage.drive_type', 'disk')
    print 'Produktname: Seriennummer'
    for device in devices:
        # get the device object
        device = dbus.Interface(
            get_object('org.freedesktop.Hal', device),
            dbus_interface='org.freedesktop.Hal.Device')
        # check if the disk is removable
        removable = device.GetPropertyBoolean('storage.removable')
        if not removable or list_removable:
            # retrieve serial number and product name
            serial = device.GetPropertyString('storage.serial')
            product = device.GetPropertyString('info.product')
            print '%s: t%s' %  (product, serial)

help = """
Usage: disk_serials [-a]

-a, --all  List serial numbers of removable drives (like card readers or usb sticks)
"""

def main():
    list_removable = False
    for arg in sys.argv:
        if arg in ('-h', '--help'):
            print help,
            sys.exit(0)
        if arg in ('-a', '--all'):
            list_removable = True
    list_devices(list_removable)

if __name__ == '__main__':
    main()
