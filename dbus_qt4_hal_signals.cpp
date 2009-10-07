// Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

// This program is free software. It comes without any warranty, to
// the extent permitted by applicable law. You can redistribute it
// and/or modify it under the terms of the Do What The Fuck You Want
// To Public License, Version 2, as published by Sam Hocevar. See
// http://sam.zoy.org/wtfpl/COPYING for more details.

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


void printError(const QDBusError &error) {
    qWarning() << error;
}


class Handler: public QObject {
    Q_OBJECT
public:
    Handler(const QDBusConnection &bus): QObject(), bus(bus) {};

public slots:
    void deviceAdded(const QString &udi);

private:
    QDBusConnection bus;
};

void Handler::deviceAdded(const QString &udi) {
    QDBusInterface device(HAL_SERVICE, udi, HAL_DEVICE_IFACE, this->bus);
    qDebug() << "device with id" << udi << "connected";
    try {
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
        printError(error);
    }
}


int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    QDBusConnection bus = QDBusConnection::systemBus();
    QDBusInterface manager(HAL_SERVICE, HAL_MANAGER_PATH,
                           HAL_MANAGER_IFACE, bus);
    Handler handler(bus);
    handler.connect(&manager, SIGNAL(DeviceAdded(const QString&)),
                    SLOT(deviceAdded(const QString&)));
    return app.exec();
}

#include "dbus_qt4_hal_signals.moc"
