#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    hal_discs
    =========

    How to retrieve the names of discs using Hal via DBus.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


from __future__ import print_function, division

from functools import partial

import dbus


def main():
    # connect to the system bus
    bus = dbus.SystemBus()
    get_object = partial(bus.get_object, 'org.freedesktop.Hal')
    # get the manager object
    manager = dbus.Interface(
        get_object('/org/freedesktop/Hal/Manager'),
        dbus_interface='org.freedesktop.Hal.Manager')
    # find all discs
    for device in manager.FindDeviceByCapability('volume.disc'):
        # get the device object
        device = dbus.Interface(get_object(device),
                                dbus_interface='org.freedesktop.Hal.Device')
        # and print the product name
        print(device.GetPropertyString('info.product'))


if __name__ == '__main__':
    main()

