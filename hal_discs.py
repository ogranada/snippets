#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from __future__ import print_function, division

from functools import partial

import dbus


def main():
    bus = dbus.SystemBus()
    get_object = partial(bus.get_object, 'org.freedesktop.Hal')
    manager = dbus.Interface(
        get_object('/org/freedesktop/Hal/Manager'),
        dbus_interface='org.freedesktop.Hal.Manager')
    for device in manager.FindDeviceByCapability('volume.disc'):
        device = dbus.Interface(get_object(device),
                                dbus_interface='org.freedesktop.Hal.Device')
        print(device.GetPropertyString('info.product'))


if __name__ == '__main__':
    main()

