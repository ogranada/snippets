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

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QtGui/QMessageBox>

MainWindow::MainWindow(QWidget *parent): QMainWindow(parent),
                                         ui(new Ui::MainWindow) {
    this->ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete this->ui;
}

void MainWindow::on_clickMe_clicked(bool isChecked) {
    const QString message = isChecked ?
        trUtf8("I am checked now.") : trUtf8("I am unchecked now");
    QMessageBox::information(this, trUtf8("You clicked me"), message);
}

void MainWindow::on_actionHello_triggered() {
    QMessageBox::information(this, trUtf8("Hello world"),
                             trUtf8("Greetings to the world."));
}

#include "mainwindow.moc"
