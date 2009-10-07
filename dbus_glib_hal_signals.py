# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from __future__ import print_function, division

from functools import partial

import dbus
from glib import MainLoop
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)


HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MANAGER_PATH = '/org/freedesktop/Hal/Manager'
HAL_MANAGER_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEVICE_IFACE = 'org.freedesktop.Hal.Device'


def device_added(bus, udi):
    device = dbus.Interface(bus.get_object(HAL_SERVICE, udi),
                            HAL_DEVICE_IFACE)
    print('device with id {0} connected.'.format(udi))
    if device.QueryCapability('volume') and device.QueryCapability('block'):
        print('\tThe device is a storage volume.')
        if device.PropertyExists('info.product'):
            name = device.GetProperty('info.product')
            print('\tProduct name: {0}'.format(name))
        else:
            print('\tThe device has no name')


def main():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(HAL_SERVICE, HAL_MANAGER_PATH),
                             HAL_MANAGER_IFACE)
    manager.connect_to_signal('DeviceAdded', partial(device_added, bus))

    mainloop = MainLoop()
    mainloop.run()


if __name__ == '__main__':
    main()
