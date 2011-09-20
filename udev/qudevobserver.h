/*
 * Copyright (c) 2011 Sebastian Wiesner <lunaryorn@googlemail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#ifndef UDEVOBSERVER_H
#define UDEVOBSERVER_H

#include "udev_auto_ptr.hpp"

#include <QtCore/QObject>

class QSocketNotifier;

/**
 * @brief Observe udev monitors and emit signals upon events.
 */
class QUDevObserver: public QObject {
   Q_OBJECT

public:
    /**
     * @brief Observe the given @p monitor.
     *
     * @param monitor the monitor to observe
     */
    explicit QUDevObserver(udev_monitor *monitor, QObject *parent=0);

    /**
     * @brief Get the observed monitor.
     *
     * @return the monitor
     */
    udev_monitor *monitor() const;

signals:
    /**
     * @brief A device changed.
     *
     * @param device the affected device
     */
    void deviceChanged(const udev_device_ptr &device);

private slots:
    /**
     * @brief Receive devices from the monitor.
     */
    void udevDataAvailable();

private:
    Q_DISABLE_COPY(QUDevObserver);

    udev_monitor_ptr m_monitor;
    QSocketNotifier *m_notifier;
};

#endif /* UDEVOBSERVER_H */
