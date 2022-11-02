# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Team\FatigueDetection\src\UI\promptWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(373, 188)
        MainWindow.move(QApplication.desktop().width()-MainWindow.width()-30,
                               1080-MainWindow.height()-60)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:15px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 351, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(8, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.titleWidget = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.titleWidget.setStyleSheet("QPushButton {\n"
"border:none;\n"
"}\n"
"QPushButton:hover {\n"
"padding-bottom:5px;\n"
"}")
        self.titleWidget.setObjectName("titleWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.titleWidget)
        self.horizontalLayout_6.setSpacing(15)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.titleLabel = QtWidgets.QLabel(self.titleWidget)
        self.titleLabel.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout_6.addWidget(self.titleLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(self.titleWidget)
        self.closeButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/images/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_6.addWidget(self.closeButton)
        self.horizontalLayout.addWidget(self.titleWidget)
        self.imgLabel = QtWidgets.QLabel(self.frame)
        self.imgLabel.setGeometry(QtCore.QRect(20, 70, 51, 51))
        self.imgLabel.setText("")
        self.imgLabel.setPixmap(QtGui.QPixmap(":/ico/images/走路.png"))
        self.imgLabel.setScaledContents(True)
        self.imgLabel.setObjectName("imgLabel")
        self.infoLabel = QtWidgets.QLabel(self.frame)
        self.infoLabel.setGeometry(QtCore.QRect(80, 70, 261, 60))
        self.infoLabel.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.closeButton.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        self.titleLabel.setText(_translate("MainWindow", f"疲劳提示"))
        self.infoLabel.setText(_translate("MainWindow", "None"))
        self.infoLabel.setWordWrap(True)


from UI import common_rc
class PromptWindow(QMainWindow):
    def __init__(self, fatigue_prompt_level=1):
        super().__init__()
        self.promptWindow = Ui_MainWindow()
        self.promptWindow.setupUi(self)
        if fatigue_prompt_level == 1:
            self.promptWindow.imgLabel.setPixmap(QtGui.QPixmap(":/ico/images/走路.png"))
            self.promptWindow.infoLabel.setText("您已经 轻度疲劳，运动一下。")
        elif fatigue_prompt_level == 2:
            self.promptWindow.imgLabel.setPixmap(QtGui.QPixmap(":/ico/images/咖啡.png"))
            self.promptWindow.infoLabel.setText("您已经 中度疲劳，喝杯咖啡。")
        elif fatigue_prompt_level == 3:
            self.promptWindow.imgLabel.setPixmap(QtGui.QPixmap(":/ico/images/床.png"))
            self.promptWindow.infoLabel.setText("您已经 重度疲劳，休息一会儿。")
        else:
            self.promptWindow.imgLabel.setPixmap(QtGui.QPixmap(":/ico/images/工人.png"))
            self.promptWindow.infoLabel.setText("当前您的状态为 清醒。")

