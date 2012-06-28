// Copyright (c) 2011 Sebastian Wiesner <lunaryorn@gmail.com>

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

#include "qudevobserver.h"

#include <QtCore/QSocketNotifier>

QUDevObserver::QUDevObserver(udev_monitor *monitor, QObject *parent) :
    QObject(parent), m_monitor(monitor) {
    udev_monitor_enable_receiving(this->m_monitor);
    this->m_notifier = new QSocketNotifier(
        udev_monitor_get_fd(this->m_monitor), QSocketNotifier::Read, this);
    connect(this->m_notifier, SIGNAL(activated(int)),
            this, SLOT(udevDataAvailable()));
}

udev_monitor *QUDevObserver::monitor() const {
    return this->m_monitor;
}

void QUDevObserver::udevDataAvailable() {
    udev_device_ptr device = udev_monitor_receive_device(this->m_monitor);
    if (!device.null()) {
        emit this->deviceChanged(device);
    }
}

#include "qudevobserver.moc"
