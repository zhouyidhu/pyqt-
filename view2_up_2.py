# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from MatplotlibWidget_2 import *


class Ui_Form_2(object):
    def setupUi(self, Form_2):
        Form_2.setObjectName("Form_2")
        Form_2.resize(427, 427)
        self.widget = MatplotlibWidget_2(Form_2)
        self.widget.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.widget.setObjectName("widget_2")

        self.retranslateUi(Form_2)
        QtCore.QMetaObject.connectSlotsByName(Form_2)

    def retranslateUi(self, Form_2):
        _translate = QtCore.QCoreApplication.translate
        Form_2.setWindowTitle(_translate("Form_2", "Form"))
