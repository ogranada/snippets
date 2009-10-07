/*
 * Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>
 *
 * This program is free software. It comes without any warranty, to
 * the extent permitted by applicable law. You can redistribute it
 * and/or modify it under the terms of the Do What The Fuck You Want
 * To Public License, Version 2, as published by Sam Hocevar. See
 * http://sam.zoy.org/wtfpl/COPYING for more details.
 */

/**
 * @file
 *
 * This file demonstrates the usage of hal signals using dbus-glib.
 */

#include <dbus/dbus-glib.h>


/** the bus name of HAL */
static const char HAL_NAME[] = "org.freedesktop.Hal";
/** the object path of the HAL Manager */
static const char HAL_MANAGER[] = "/org/freedesktop/Hal/Manager";
/** the manager interface */
static const char HAL_MANAGER_IFACE[] = "org.freedesktop.Hal.Manager";
/** the device interface */
static const char HAL_DEVICE_IFACE[] = "org.freedesktop.Hal.Device";


/**
 * @brief Print the specified @p error.
 *
 * DBus exceptions are formatted differently from normal errors.
 *
 * @param error the error to print
 */
void print_error(GError *error) {
    if (!error)
        return;
    if (error->domain == DBUS_GERROR &&
        error->code == DBUS_GERROR_REMOTE_EXCEPTION) {
        g_printerr("Exception %s: %s\n",
                   dbus_g_error_get_name(error),
                   error->message);
    } else {
        g_printerr("%s\n", error->message);
    }
}


/**
 * @brief Check, if @p property exists on @p device.
 *
 * @param device the device
 * @param property the name of the property to check for
 * @param error a GError pointer set in case of errors
 * @return @c TRUE, if @p property exists, @c FALSE otherwise.
 */
gboolean device_property_exists(DBusGProxy *device, gchar *property,
                                GError **error) {
    gboolean exists = FALSE;
    /* First parameter is the dbus object, second the method name, third the
       error pointer.  G_TYPE_INVALID marks the end of argument lists. */
    dbus_g_proxy_call(device, "PropertyExists", error,
                      /** the input arguments */
                      G_TYPE_STRING, property, G_TYPE_INVALID,
                      /** the return values */
                      G_TYPE_BOOLEAN, &exists, G_TYPE_INVALID);
    return exists;
}


/**
 * @brief Get the string value of @p property on @p device.
 *
 * @param device the device
 * @param property the name of the property to query
 * @param error a GError pointer set in case of errors
 * @return the property value
 */
gchar *device_get_property_string(DBusGProxy *device, gchar *property,
                                  GError **error) {
    gchar *value = NULL;
    dbus_g_proxy_call(device, "GetPropertyString", error,
                      G_TYPE_STRING, property, G_TYPE_INVALID,
                      G_TYPE_STRING, &value, G_TYPE_INVALID);
    return value;
}


/**
 * @brief Query a @p capability of @p device.
 *
 * Capabilities inform about what a device can do.  Mouse devices have the
 * "input.touchpad" capability, volumes on removable media have "volume" and
 * "block" capabilities, whereas the removable device itself has "storage"
 * and "block" capabilities.
 *
 * @param device the device
 * @param capability the capability to query
 * @param error a GError pointer set in case of errors
 * @return @c TRUE, if the @p device has the @p capability, @c FALSE
 *         otherwise
 */
gboolean device_query_capability(DBusGProxy *device, gchar *capability,
                                 GError **error) {
    gboolean has_capability = FALSE;
    dbus_g_proxy_call(device, "QueryCapability", error,
                      G_TYPE_STRING, capability, G_TYPE_INVALID,
                      G_TYPE_BOOLEAN, &has_capability, G_TYPE_INVALID);
    return has_capability;
}


/**
 * @brief Signal handler for @c DeviceAdded.
 *
 * @param manager the manager, from which the signal originated
 * @param udi the universal device id of the device, that was added
 * @param bus the bus connection
 */
void device_added(DBusGProxy *manager, gchar *udi, DBusGConnection *bus) {
    GError *error = NULL;
    gchar *name = NULL;
    gboolean is_volume = FALSE;
    gboolean is_block = FALSE;
    /* get the dbus object for the added device */
    DBusGProxy *device = dbus_g_proxy_new_for_name(bus, HAL_NAME, udi,
                                                   HAL_DEVICE_IFACE);

    g_print("device with id %s connected.\n", udi);
    is_volume = device_query_capability(device, "volume", &error);
    if (error)
        goto unwind;
    is_block = device_query_capability(device, "block", &error);
    if (error)
        goto unwind;
    if (is_volume && is_block) {
        g_print("\tThe device is a storage volume.\n");
        /* print the product name of the device, if it has one.  Use the
           hal-device command to list properties of devices. */
        if (device_property_exists(device, "info.product", &error)) {
            if (error)
                goto unwind;
            name = device_get_property_string(device, "info.product",
                                              &error);
            if (error)
                goto unwind;
            g_print("\tProduct name: %s\n", name);
        }
    }
unwind:
    /* cleanup */
    g_free(name);
    if (device)
        g_object_unref(device);
    if (error) {
        print_error(error);
        g_error_free(error);
    }
}


int main(void) {
    DBusGConnection *bus = NULL;
    GError *error = NULL;
    DBusGProxy *manager = NULL;
    GMainLoop *mainloop = NULL;

    /* initialize the GObject type system.  Mandatory for every Glib
     * program */
    g_type_init();

    /* connect to the system bus.  System services like HAL oder
     * NetworkManager live on this bus, the session bus (DBUS_BUS_SESSION)
     * houses per-user applications like media players */
    bus = dbus_g_bus_get(DBUS_BUS_SYSTEM, &error);
    if (error)
        goto unwind;

    /* get the hal manager object.  This object maintains a list of all
     * connected devices and notifies clients about changes. */
    manager = dbus_g_proxy_new_for_name(bus, HAL_NAME, HAL_MANAGER,
                                        HAL_MANAGER_IFACE);
    /* inform the GObject signal subsystem about the signature of the
     * DeviceAdded signal.  This is required for proper unmarshalling of
     * arguments into c types. */
    dbus_g_proxy_add_signal(manager, "DeviceAdded", G_TYPE_STRING,
                            G_TYPE_INVALID);
    /* connect our callback to the signal.  The fourth argument is a void
     * pointer, which passes arbitrary data to the signal handler upon
     * invocation.  We use this to pass the bus connection to the signal
     * handler. */
    dbus_g_proxy_connect_signal(manager, "DeviceAdded",
                                G_CALLBACK(device_added), bus, NULL);

    /* create and run the main loop to handle incoming signals */
    mainloop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(mainloop);

unwind:
    /* cleanup stuff */
    if (mainloop)
        g_main_loop_unref(mainloop);
    if (manager)
        g_object_unref(manager);
    if (bus)
        dbus_g_connection_unref(bus);
    if (error) {
        print_error(error);
        g_error_free(error);
    }
    return 0;
}
