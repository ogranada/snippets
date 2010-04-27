// Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

// This program is free software. It comes without any warranty, to
// the extent permitted by applicable law. You can redistribute it
// and/or modify it under the terms of the Do What The Fuck You Want
// To Public License, Version 2, as published by Sam Hocevar. See
// http://sam.zoy.org/wtfpl/COPYING for more details.


/**
 * @file
 *
 * Demonstrates the connection to HAL signals using C++ and Qt4.
 */


static const char HAL_SERVICE[] = "org.freedesktop.Hal";
static const char HAL_MANAGER_PATH[] = "/org/freedesktop/Hal/Manager";
static const char HAL_MANAGER_IFACE[] = "org.freedesktop.Hal.Manager";
static const char HAL_DEVICE_IFACE[] = "org.freedesktop.Hal.Device";


#include <QtCore/QObject>
#include <QtCore/QCoreApplication>
#include <QtCore/QtDebug>
#include <QtDBus/QDBusConnection>
#include <QtDBus/QDBusInterface>
#include <QtDBus/QDBusReply>


/**
 * @brief This class will handle incoming signals
 */
class Handler: public QObject {
    Q_OBJECT
public:
    /**
     * @brief Construct a new handler
     *
     * @param bus the bus, from which the signals will be send
     */
    Handler(const QDBusConnection &bus): QObject(), bus(bus) {};

public slots:
    /**
     * Called, if the DeviceAdded signal is emitted.
     *
     * @param udi the device id
     */
    void deviceAdded(const QString &udi);

private:
    QDBusConnection bus;
};

void Handler::deviceAdded(const QString &udi) {
    /* get the dbus object for the new device */
    QDBusInterface device(HAL_SERVICE, udi, HAL_DEVICE_IFACE, this->bus);
    qDebug() << "device with id" << udi << "connected";
    try {
        /* check the capabilities of the device, only volumes on block
         * devices are handled. */
        QDBusReply<bool> isVolume = device.call("QueryCapability",
                                                "volume");
        if (!isVolume.isValid())
            throw isVolume.error();

        QDBusReply<bool> isBlock = device.call("QueryCapability",
                                               "block");
        if (!isBlock.isValid())
            throw isBlock.error();

        if (isVolume.value() && isBlock.value()) {
            qDebug() << "\tThe device is a storage volume";
            /* print the product name, if the device has one.*/
            QDBusReply<bool> hasProductName = device.call("PropertyExists",
                                                          "info.product");
            if (!hasProductName.isValid())
                throw hasProductName.error();
            if (hasProductName.value()) {
                QDBusReply<QString> productName = device.call(
                    "GetPropertyString", "info.product");
                if (!productName.isValid())
                    throw productName.error();
                qDebug() << "\tProduct name:" << productName.value();
            } else {
                qDebug() << "\tThe device has no name";
            }
        }
    } catch (const QDBusError &error) {
        qWarning() << error;
    }
}


int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    /* Connect to the system bus, which provides system services like HAL or
     * NetworkManager.  The session bus */
    QDBusConnection bus = QDBusConnection::systemBus();
    /* get the hal manager object on this bus.  This object maintains a list
     * of devices and notifies clients about changes. */
    QDBusInterface manager(HAL_SERVICE, HAL_MANAGER_PATH,
                           HAL_MANAGER_IFACE, bus);
    /* connect to the DeviceAdded signal */
    Handler handler(bus);
    handler.connect(&manager, SIGNAL(DeviceAdded(const QString&)),
                    SLOT(deviceAdded(const QString&)));
    /* start looping to handle incoming signals */
    return app.exec();
}

#include "dbus_qt4_hal_signals.moc"
