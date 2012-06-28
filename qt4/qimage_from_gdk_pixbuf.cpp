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

/**
 * @brief Conversion of GDK pixel buffers to QImage.
 */

extern "C" {
#include <glib.h>
#include <gdk-pixbuf/gdk-pixbuf.h>
}

#include <QtGui/QApplication>
#include <QtGui/QImage>
#include <QtGui/QLabel>
#include <QtCore/QStringList>
#include <QtCore/QTextStream>
#include <QtCore/QtDebug>


/**
 * @brief Convert a GdkPixbuf to a QImage.
 *
 * @param pixbuf the GdkPixbuf to convert
 * @return the converted image, or a null QImage in case of error
 */
QImage toQImage(GdkPixbuf *pixbuf) {
    gchar *buffer;
    gsize buffer_size;
    GError *error = 0;
    const gboolean success = gdk_pixbuf_save_to_buffer(
        pixbuf, &buffer, &buffer_size, "png", &error, NULL);
    if (!success) {
        Q_ASSERT(error);
        qWarning() << "conversion failed:" << error->message;
        g_error_free(error);
        return QImage();
    } else {
        // wrap pointers into byte array to avoid sign issues:  The buffer is
        // plain "char", but "QImage::loadFromData()" expects "unsigned char".
        // Thus we wrap the buffer into a QByteArray which uses plain "char",
        // too.  By using "fromRawData()" instead of the constructor we avoid a
        // superfluous copy of image data.
        const QByteArray data = QByteArray::fromRawData(buffer, buffer_size);
        QImage image;
        image.loadFromData(data);
        g_free(buffer);
        return image;
    }
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    g_type_init();

    const QStringList arguments = app.arguments();
    const QString progname = arguments.value(0);
    const QString filename = arguments.value(1);
    if (filename.isNull()) {
        QTextStream err(stderr);
        err << "usage: " << progname << " filename" << endl;
        return EXIT_FAILURE;
    }

    GError *error = 0;
    GdkPixbuf *pixbuf = gdk_pixbuf_new_from_file(
        filename.toUtf8(), &error);
    if (error) {
        QTextStream err(stderr);
        err << QString::fromUtf8(error->message) << endl;
        g_error_free(error);
        return EXIT_FAILURE;
    }

    QImage image = toQImage(pixbuf);
    QLabel label;
    label.setPixmap(QPixmap::fromImage(image));
    label.show();

    return app.exec();
}

