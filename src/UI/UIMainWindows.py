# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './MainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(518, 707)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 521, 431))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/images/main.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 460, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 460, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 520, 451, 161))
        self.label_2.setStyleSheet("border:1px solid black;")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "疲劳检测测试样机"))
        self.pushButton.setText(_translate("Form", "开始检测"))
        self.pushButton_2.setText(_translate("Form", "停止检测"))
        self.label_2.setText(_translate("Form", "测试样机"))

        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.pushButton_2.setDisabled(True)

from UI import common_rc
