# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server_window_template.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QTextEdit, QWidget)

class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        if not ServerWindow.objectName():
            ServerWindow.setObjectName(u"ServerWindow")
        ServerWindow.resize(1900, 1008)
        self.centralwidget = QWidget(ServerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 1900, 981))
        self.label.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.721889, y1:0.211, x2:0.917, y2:0.772591, stop:0.0111111 rgba(56, 56, 56, 255), stop:0.744444 rgba(95, 95, 95, 255));")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(60, 20, 1631, 911))
        self.scrollArea.setMinimumSize(QSize(1515, 800))
        self.scrollArea.setMaximumSize(QSize(16777215, 1000))
        self.scrollArea.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgba(122, 122, 122, 50%);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1631, 911))
        self.found_frame = QFrame(self.scrollAreaWidgetContents)
        self.found_frame.setObjectName(u"found_frame")
        self.found_frame.setGeometry(QRect(110, 70, 1421, 251))
        self.found_frame.setMinimumSize(QSize(0, 0))
        self.found_frame.setMaximumSize(QSize(2000, 2000))
        self.found_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.found_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.found_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_3 = QLabel(self.found_frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 20, 221, 31))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(20)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.active_works_tableWidget = QTableWidget(self.found_frame)
        self.active_works_tableWidget.setObjectName(u"active_works_tableWidget")
        self.active_works_tableWidget.setGeometry(QRect(55, 60, 1311, 171))
        self.need_frame = QFrame(self.scrollAreaWidgetContents)
        self.need_frame.setObjectName(u"need_frame")
        self.need_frame.setGeometry(QRect(110, 350, 1421, 251))
        self.need_frame.setMinimumSize(QSize(0, 0))
        self.need_frame.setMaximumSize(QSize(2000, 500))
        self.need_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.need_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.need_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_5 = QLabel(self.need_frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 20, 221, 31))
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.data_base_tableWidget = QTableWidget(self.need_frame)
        self.data_base_tableWidget.setObjectName(u"data_base_tableWidget")
        self.data_base_tableWidget.setGeometry(QRect(60, 60, 1311, 171))
        self.status_label = QLabel(self.scrollAreaWidgetContents)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(50, 10, 291, 41))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(26)
        font1.setBold(True)
        self.status_label.setFont(font1)
        self.status_label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.need_frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.need_frame_2.setObjectName(u"need_frame_2")
        self.need_frame_2.setGeometry(QRect(110, 630, 1421, 251))
        self.need_frame_2.setMinimumSize(QSize(0, 0))
        self.need_frame_2.setMaximumSize(QSize(2000, 500))
        self.need_frame_2.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.need_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.need_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_6 = QLabel(self.need_frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(50, 20, 221, 31))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.server_logs_textEdit = QTextEdit(self.need_frame_2)
        self.server_logs_textEdit.setObjectName(u"server_logs_textEdit")
        self.server_logs_textEdit.setGeometry(QRect(60, 60, 1311, 171))
        self.server_logs_textEdit.setReadOnly(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.back_pushButton = QPushButton(self.centralwidget)
        self.back_pushButton.setObjectName(u"back_pushButton")
        self.back_pushButton.setGeometry(QRect(1710, 850, 181, 81))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(24)
        font2.setBold(True)
        self.back_pushButton.setFont(font2)
        self.back_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.back_pushButton.setText(u"Stop")
        self.back_pushButton.setIconSize(QSize(80, 80))
        self.back_pushButton.setAutoRepeat(True)
        self.start_pushButton = QPushButton(self.centralwidget)
        self.start_pushButton.setObjectName(u"start_pushButton")
        self.start_pushButton.setGeometry(QRect(1710, 740, 181, 81))
        self.start_pushButton.setFont(font2)
        self.start_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.start_pushButton.setText(u"Start")
        self.start_pushButton.setIconSize(QSize(80, 80))
        self.start_pushButton.setAutoRepeat(True)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ServerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1900, 33))
        self.menuConfiguracion = QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(u"menuConfiguracion")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        ServerWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ServerWindow)
        self.statusbar.setObjectName(u"statusbar")
        ServerWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuConfiguracion.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(ServerWindow)

        QMetaObject.connectSlotsByName(ServerWindow)
    # setupUi

    def retranslateUi(self, ServerWindow):
        ServerWindow.setWindowTitle(QCoreApplication.translate("ServerWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_3.setText(QCoreApplication.translate("ServerWindow", u"Active Works", None))
        self.label_5.setText(QCoreApplication.translate("ServerWindow", u"Data Base", None))
        self.status_label.setText(QCoreApplication.translate("ServerWindow", u"Status:  OFF", None))
        self.label_6.setText(QCoreApplication.translate("ServerWindow", u"Server Logs", None))
        self.menuConfiguracion.setTitle(QCoreApplication.translate("ServerWindow", u"Configuracion", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("ServerWindow", u"Ayuda", None))
    # retranslateUi

