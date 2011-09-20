// Copyright (c) 2010, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

// This program is free software. It comes without any warranty, to
// the extent permitted by applicable law. You can redistribute it
// and/or modify it under the terms of the Do What The Fuck You Want
// To Public License, Version 2, as published by Sam Hocevar. See
// http://sam.zoy.org/wtfpl/COPYING for more details.

/**
 * @brief Monitor devices with libudev and Qt.
 */

#include "udev_monitor.h"
#include "qudevobserver.h"

#include <QtCore/QTextStream>
#include <QtCore/QByteArray>
#include <QtCore/QCoreApplication>

void MouseMonitor::mouseChanged(const udev_device_ptr &device) {
    QTextStream out(stdout);
    QByteArray action = udev_device_get_action(device);
    QByteArray isMouse = udev_device_get_property_value(
        device, "ID_INPUT_MOUSE");
    QByteArray sysName = udev_device_get_sysname(device);
    if (isMouse == "1" && sysName.indexOf("event") == 0) {
        udev_device_ptr parent = udev_device_get_parent(device);
        // device pointer has no initial reference, so forcibly acquire
        // a reference
        parent.ref();
        if (parent) {
            QByteArray name = udev_device_get_property_value(
                parent, "NAME");
            if (!name.isEmpty()) {
                if (action == "add") {
                    out << name << " added" << endl;
                } else if (action == "remove") {
                    out << name << " removed" << endl;
                }
            }
        }
    }
}

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    udev_ptr context = udev_new();
    udev_monitor_ptr monitor = udev_monitor_new_from_netlink(context, "udev");
    udev_monitor_filter_add_match_subsystem_devtype(monitor, "input", 0);
    QUDevObserver observer(monitor);
    MouseMonitor client;
    QObject::connect(&observer, SIGNAL(deviceChanged(const udev_device_ptr&)),
                     &client, SLOT(mouseChanged(const udev_device_ptr&)));
    return app.exec();
}

#include "udev_monitor.moc"
