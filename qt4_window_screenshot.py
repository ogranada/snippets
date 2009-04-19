#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess

from PyQt4 import QtGui, QtCore


class MyMainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        central = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout(central)
        self.image_label = QtGui.QLabel('here\'s the shot', central)
        layout.addWidget(self.image_label)
        self.button = QtGui.QPushButton('Shoot me!', central)
        self.button.setObjectName('shot_button')
        layout.addWidget(self.button)
        self.setCentralWidget(central)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSignature('')
    def on_shot_button_clicked(self):
        # using import from ImageMagick
        # proc = subprocess.Popen(
        #     ['import', '-silent', '-window', str(self.winId()), 'png:-'],
        #     stdout=subprocess.PIPE)
        # stdout = proc.communicate()[0]
        # image = QtGui.QImage()
        # image.loadFromData(stdout)
        # self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))

        # correct way!
        self.image_label.setPixmap(QtGui.QPixmap.grabWidget(self))



def main():
    app = QtGui.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

