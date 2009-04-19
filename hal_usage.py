#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Uses the hal dbus api to obtain the serials of all storage devices
# Copyright (c) 2007 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import sys
import dbus


def list_devices(list_removable=False):
    bus = dbus.SystemBus()
    proxy_obj = bus.get_object('org.freedesktop.Hal',
                               '/org/freedesktop/Hal/Manager')
    hal_manager = dbus.Interface(proxy_obj, 'org.freedesktop.Hal.Manager')
    devs = hal_manager.FindDeviceStringMatch('storage.drive_type', 'disk')
    print 'Produktname: Seriennummer'
    for dev in devs:
        p_obj = bus.get_object('org.freedesktop.Hal', dev)
        dev_iface = dbus.Interface(p_obj, 'org.freedesktop.Hal.Device')
        removable = dev_iface.GetPropertyBoolean('storage.removable')
        if not removable or list_removable:
            serial = dev_iface.GetPropertyString('storage.serial')
            product = dev_iface.GetPropertyString('info.product')
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
