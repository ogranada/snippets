// Copyright (c) 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

/**
 * @brief Use libudev for device enumeration.
 *
 * Enumerate all mouse devices and print product name and type (touchpad or
 * not).
 */

#include "udev_auto_ptr.hpp"

#include <iostream>


int main() {
    using namespace std;

    // get a udev handle.  This is required for all libudev operations
    udev_ptr context = udev_new();

    // scan input subsystem for mouse devices
    udev_enumerate_ptr enumerator = udev_enumerate_new(context);
    udev_enumerate_add_match_subsystem(enumerator, "input");
    udev_enumerate_add_match_property(enumerator, "ID_INPUT_MOUSE", "1");
    udev_enumerate_scan_devices(enumerator);

    // iterate over the device list using a convenient iteration macro from
    // libudev.  The entry name is the sysfs path of the device.
    udev_list_entry *devices = udev_enumerate_get_list_entry(enumerator);
    udev_list_entry *current_entry;
    udev_list_entry_foreach(current_entry, devices) {
        // "open" the device from the sysfs path, so that we can access its
        // metadata
        udev_device_ptr device = udev_device_new_from_syspath(
            context, udev_list_entry_get_name(current_entry));
        // handle the generic event device only, not "mouse" device nodes (some
        // mouse devices are represented by two device nodes)
        string name = udev_device_get_sysname(device);
        if (name.find("event") == 0) {
            udev_device_ptr parent = udev_device_get_parent(device);
            // forcibly acquire reference to parent, because parent's ref-count
            // is 0
            parent.ref();
            cout << udev_device_get_property_value(parent, "NAME");
            const char *is_touchpad = udev_device_get_property_value(
                device, "ID_INPUT_TOUCHPAD");
            // ID_INPUT_TOUCHPAD is either 0 or unset if the device is not a
            // touchpad.
            if (is_touchpad && is_touchpad[0] == '1') {
                cout << " (touchpad)";
            }
            cout << endl;
        }
    }
   return 0;
}
