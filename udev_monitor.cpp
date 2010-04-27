// Copyright (c) 2010 Sebastian Wiesner <lunaryorn@googlemail.com>

// This program is free software. It comes without any warranty, to
// the extent permitted by applicable law. You can redistribute it
// and/or modify it under the terms of the Do What The Fuck You Want
// To Public License, Version 2, as published by Sam Hocevar. See
// http://sam.zoy.org/wtfpl/COPYING for more details.

/**
 * This snippet monitors devices using libudev.
 */


extern "C" {
#include <libudev.h>
}

#include <QtCore/QSocketNotifier>
#include <QtCore/QTextStream>
#include <QtCore/QCoreApplication>
#include <QtCore/QByteArray>


template<class T, T* (*Ref)(T*), void (*Unref)(T*)> class QUDevPointer {
public:
    QUDevPointer(): m_ptr(0) {
    }

    QUDevPointer(const QUDevPointer<T, Ref, Unref> &other) {
        this->m_ptr = other.m_ptr;
        Ref(this->m_ptr);
    }

    QUDevPointer(T *ptr) {
        this->m_ptr = ptr;
    }

    ~QUDevPointer() {
        Unref(this->m_ptr);
    }

    QUDevPointer &operator=(const QUDevPointer<T, Ref, Unref> &other) {
        Unref(this->m_ptr);
        this->m_ptr = other->m_ptr;
        Ref(this->m_ptr);
        return *this;
    }

    QUDevPointer &operator=(T *ptr) {
        if (this->m_ptr)
            Unref(this->m_ptr);
        this->m_ptr = ptr;
        return *this;
    }

    void ref() {
        Ref(this->m_ptr);
    }

    void unref() {
        Unref(this->m_ptr);
    }

    operator T*() const {
        return this->m_ptr;
    }

    operator bool() const {
        return this->m_ptr;
    }

    T *data() const {
        return this->m_ptr;
    }

    bool isNull() const {
        return !this->m_ptr;
    }

private:
    T *m_ptr;
};


typedef QUDevPointer<struct udev, udev_ref, udev_unref> QUDevPtr;
typedef QUDevPointer<struct udev_monitor, udev_monitor_ref,
                     udev_monitor_unref> QUDevMonitorPtr;
typedef QUDevPointer<struct udev_device, udev_device_ref,
                     udev_device_unref> QUDevDevicePtr;


class QUDevClient: public QObject {
    Q_OBJECT
public:
    QUDevClient(QObject *parent=0);

private Q_SLOTS:
    void udevDataAvailable();

private:
    Q_DISABLE_COPY(QUDevClient);

    QUDevPtr context;
    QUDevMonitorPtr monitor;
    QSocketNotifier *monitorNotifier;
};


void QUDevClient::udevDataAvailable() {
    QTextStream out(stdout);

    QUDevDevicePtr device = udev_monitor_receive_device(this->monitor);
    if (device) {
        QByteArray action = udev_device_get_action(device);
        QByteArray isMouse = udev_device_get_property_value(
            device, "ID_INPUT_MOUSE");
        QByteArray sysName = udev_device_get_sysname(device);
        if (isMouse == "1" && sysName.indexOf("mouse") == 0) {
            QUDevDevicePtr parent = udev_device_get_parent(device);
            // device pointer has no initial reference, so forcibly acquire
            // a reference
            parent.ref();
            if (parent) {
                QByteArray name = udev_device_get_property_value(parent,
                                                                 "NAME");
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
}

QUDevClient::QUDevClient(QObject *parent): QObject(parent) {
    this->context = udev_new();
    this->monitor = udev_monitor_new_from_netlink(this->context, "udev");
    udev_monitor_filter_add_match_subsystem_devtype(
        this->monitor, "input", 0);
    udev_monitor_enable_receiving(this->monitor);
    this->monitorNotifier = new QSocketNotifier(
        udev_monitor_get_fd(this->monitor), QSocketNotifier::Read, this);
    connect(this->monitorNotifier, SIGNAL(activated(int)),
            this, SLOT(udevDataAvailable()));
}


int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    QUDevClient client;
    return app.exec();
}

#include "udev_monitor.moc"
