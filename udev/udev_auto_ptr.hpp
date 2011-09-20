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

#ifndef UDEV_AUTO_PTR_H
#define UDEV_AUTO_PTR_H

extern "C" {
#include <libudev.h>
}

/**
 * @brief Auto pointer for udev structures.
 *
 * This auto pointer type wraps udev reference counting semantics.
 *
 * @param T the udev type
 * @param Ref function to take a reference to T
 * @param Unref function to release a reference to T
 */
template<class T, T* (*Ref)(T*), void (*Unref)(T*)> class udev_auto_ptr {
public:
    /**
     * @brief Null pointer.
     */
    udev_auto_ptr(): m_ptr(0) {
    }

    /**
     * @brief Copy constructor.
     *
     * @param other another pointer
     */
    udev_auto_ptr(const udev_auto_ptr<T, Ref, Unref> &other) {
        this->m_ptr = other.m_ptr;
        Ref(this->m_ptr);
    }

    /**
     * @brief Wrap a raw pointer.
     *
     * The reference count of @p ptr is @em not modified.
     *
     * @param ptr a raw pointer
     */
    udev_auto_ptr(T *ptr) {
        this->m_ptr = ptr;
    }

    ~udev_auto_ptr() {
        Unref(this->m_ptr);
    }

    /**
     * @brief Copy assignment operator.
     *
     * @param other other pointer
     * @return reference to this pointer
     */
    udev_auto_ptr &operator=(const udev_auto_ptr<T, Ref, Unref> &other) {
        Unref(this->m_ptr);
        this->m_ptr = other->m_ptr;
        Ref(this->m_ptr);
        return *this;
    }

    /**
     * @brief Assign a raw pointer.
     *
     * The reference count of @p ptr is @em not modified.
     *
     * @param ptr a raw pointer
     * @return reference to this pointer
     */
    udev_auto_ptr &operator=(T *ptr) {
        if (this->m_ptr)
            Unref(this->m_ptr);
        this->m_ptr = ptr;
        return *this;
    }

    /**
     * @brief Forcibly increase reference count of the wrapped pointer.
     */
    void ref() {
        Ref(this->m_ptr);
    }

    /**
     * @brief Forcibly decrease reference count of the wrapped pointer.
     *
     * This function deletes the underlying object @em without notice, if the
     * reference count drops to zero.  Subsequent access to this pointer is
     * undefined afterwards.  Use with care!
     */
    void unref() {
        Unref(this->m_ptr);
    }

    /**
     * @brief Cast to raw pointer.
     *
     * @return the wrapped pointer, or 0, if this is a null pointer
     */
    operator T*() const {
        return this->m_ptr;
    }

    /**
     * @brief Cast to bool
     *
     * @return @c true, if this pointer is non-zero, @c false otherwise.
     */
    operator bool() const {
        return this->m_ptr;
    }

    /**
     * @brief Get the wrapped pointer.
     *
     * @return the wrapped pointer, or 0, if this is a null pointer
     */
    T *data() const {
        return this->m_ptr;
    }

    /**
     * @brief Is this a null pointer?
     *
     * @return @c true, if this pointer is a null pointer, @c false otherwise
     */
    bool null() const {
        return !this->m_ptr;
    }

private:
    T *m_ptr;
};

/**
 * @brief Auto pointer to @c udev.
 */
typedef udev_auto_ptr<struct udev, udev_ref, udev_unref> udev_ptr;

/**
 * @brief Auto pointer to @c udev_enumerate.
 */
typedef udev_auto_ptr<struct udev_enumerate, udev_enumerate_ref,
                      udev_enumerate_unref> udev_enumerate_ptr;

/**
 * @brief Auto pointer to @c udev_monitor.
 */
typedef udev_auto_ptr<struct udev_monitor, udev_monitor_ref,
                      udev_monitor_unref> udev_monitor_ptr;

/**
 * @brief Auto pointer to @c udev_device.
 */
typedef udev_auto_ptr<struct udev_device, udev_device_ref,
                      udev_device_unref> udev_device_ptr;

#endif /* UDEV_AUTO_PTR_H */
