# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jack/WorkSpace/pyutils/testM/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(517, 96)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label.setObjectName("label")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(109, 18, 118, 22))
        self.timeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(6, 0, 0)))
        self.timeEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.timeEdit.setCalendarPopup(False)
        self.timeEdit.setTime(QtCore.QTime(6, 0, 0))
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setGeometry(QtCore.QRect(280, 18, 118, 22))
        self.timeEdit_2.setCalendarPopup(False)
        self.timeEdit_2.setTime(QtCore.QTime(6, 30, 0))
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(246, 22, 54, 12))
        self.label_2.setObjectName("label_2")
        self.main = QtWidgets.QPushButton(self.centralwidget)
        self.main.setGeometry(QtCore.QRect(420, 18, 75, 23))
        self.main.setMouseTracking(False)
        self.main.setFlat(False)
        self.main.setObjectName("main")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 517, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.main.clicked.connect(MainWindow.onStar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "每天录制时间："))
        self.label_2.setText(_translate("MainWindow", "至"))
        self.main.setText(_translate("MainWindow", "开始"))
