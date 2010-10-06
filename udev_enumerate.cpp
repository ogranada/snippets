// Copyright (c) 2010 Sebastian Wiesner <lunaryorn@googlemail.com>

// This program is free software. It comes without any warranty, to
// the extent permitted by applicable law. You can redistribute it
// and/or modify it under the terms of the Do What The Fuck You Want
// To Public License, Version 2, as published by Sam Hocevar. See
// http://sam.zoy.org/wtfpl/COPYING for more details.

// libudev is LGPL (by license header in libudev.h), so we are free in
// choice of license!

/**
 * This snippet demonstrates the use of libudev for enumeration of devices.
 * It enumerates all mouse devices and prints the product name and whether
 * the mouse is a touchpad or not.
 */

#include <iostream>

extern "C" {
#include <libudev.h>
}


int main() {
    using namespace std;

    // get us "connected" to the udev library.  This context is required for
    // all library operations.
    struct udev *context = udev_new();

    // create a new "enumeration context".  We can gradually add matches or
    // nomatches for properties or subsystem or whatever (see documentation)
    // and finally scan for matching devices or subsystems.  After we have
    // scanned, we can turn the enumerator into a list and loop over it.
    struct udev_enumerate *enumerator = udev_enumerate_new(context);
    // input devices only
    udev_enumerate_add_match_subsystem(enumerator, "input");
    // mouse devices only
    udev_enumerate_add_match_property(enumerator, "ID_INPUT_MOUSE", "1");
    // now scan
    udev_enumerate_scan_devices(enumerator);
    // and create a list of all scan results.
    struct udev_list_entry *device_entries = udev_enumerate_get_list_entry(
        enumerator);

    // iterate over the device list using a convenient iteration macro from
    // libudev.  The "name" of each list entry is the sysfs path of the
    // device, the value is apparently (proven by experiments, not by
    // documentation!) undefined for device lists.
    struct udev_list_entry *current_entry;
    udev_list_entry_foreach(current_entry, device_entries) {
        // "open" the device from the sysfs path, so that we can access its
        // metadata
        struct udev_device *device = udev_device_new_from_syspath(
            context, udev_list_entry_get_name(current_entry));
        // get the sysfs name of the device
        string name = udev_device_get_sysname(device);
        // check, if the device name starts with "mouse".  Only these are
        // mouse devices (not, for instance, event devices)
        if (name.find("mouse") == 0) {
            // get the parent device.  This is the physical device, which we
            // are interested in.
            struct udev_device *parent = udev_device_get_parent(device);
            // print the device name
            cout << udev_device_get_property_value(parent, "NAME");
            // and check if its a touchpad
            const char *is_touchpad = udev_device_get_property_value(
                device, "ID_INPUT_TOUCHPAD");
            // if the device is not a touchpad, the ID_INPUT_TOUCHPAD
            // property may either be unset or 0, so check against these
            // cases (again, proven by experiments, not by reference)
            if (is_touchpad && is_touchpad[0] == '1') {
                // it is a touchpad
                cout << " (touchpad)";
            }
            cout << endl;
        }
        // remove our reference to this device, libudev will do the cleaning
        // up
        udev_device_unref(device);
    }
    // we are done with enumerator, so free the enumerator context.  This
    // invalidates the device list!
    udev_enumerate_unref(enumerator);

    // we are done with libudev in general, so cleanup the whole library.
    // don't know, what this actually frees, but it is obviously required.
    udev_unref(context);

    // bail out
    return 0;
}
