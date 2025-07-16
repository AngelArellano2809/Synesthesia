# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_songrzJbnw.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QWidget)

class Ui_NewSongWindow(object):
    def setupUi(self, NewSongWindow):
        if not NewSongWindow.objectName():
            NewSongWindow.setObjectName(u"NewSongWindow")
        NewSongWindow.resize(1900, 1010)
        self.centralwidget = QWidget(NewSongWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 1900, 981))
        self.label.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.721889, y1:0.211, x2:0.917, y2:0.772591, stop:0.0111111 rgba(56, 56, 56, 255), stop:0.744444 rgba(95, 95, 95, 255));")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(213, 80, 1515, 922))
        self.scrollArea.setMinimumSize(QSize(1515, 922))
        self.scrollArea.setMaximumSize(QSize(16777215, 770))
        self.scrollArea.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgba(122, 122, 122, 50%);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1515, 922))
        self.file_pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.file_pushButton.setObjectName(u"file_pushButton")
        self.file_pushButton.setGeometry(QRect(430, 140, 321, 121))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        font.setBold(True)
        self.file_pushButton.setFont(font)
        self.file_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.file_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.file_pushButton.setText(u"Select File")
        self.file_pushButton.setIconSize(QSize(80, 80))
        self.file_pushButton.setAutoRepeat(True)
        self.found_frame = QFrame(self.scrollAreaWidgetContents)
        self.found_frame.setObjectName(u"found_frame")
        self.found_frame.setGeometry(QRect(110, 300, 1311, 260))
        self.found_frame.setMinimumSize(QSize(0, 0))
        self.found_frame.setMaximumSize(QSize(2000, 2000))
        self.found_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.found_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.found_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.need_frame = QFrame(self.scrollAreaWidgetContents)
        self.need_frame.setObjectName(u"need_frame")
        self.need_frame.setGeometry(QRect(110, 590, 1311, 260))
        self.need_frame.setMinimumSize(QSize(0, 0))
        self.need_frame.setMaximumSize(QSize(1374, 300))
        self.need_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.need_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.need_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.add_pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.add_pushButton.setObjectName(u"add_pushButton")
        self.add_pushButton.setGeometry(QRect(770, 140, 321, 121))
        self.add_pushButton.setFont(font)
        self.add_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.add_pushButton.setText(u"Add")
        self.add_pushButton.setIconSize(QSize(80, 80))
        self.add_pushButton.setAutoRepeat(True)
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(510, 20, 501, 81))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(48)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0%);")
        self.image_label = QLabel(self.scrollAreaWidgetContents)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(110, 30, 241, 241))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.back_pushButton = QPushButton(self.centralwidget)
        self.back_pushButton.setObjectName(u"back_pushButton")
        self.back_pushButton.setGeometry(QRect(20, 850, 181, 81))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(24)
        font2.setBold(True)
        self.back_pushButton.setFont(font2)
        self.back_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.back_pushButton.setText(u"Back")
        self.back_pushButton.setIconSize(QSize(80, 80))
        self.back_pushButton.setAutoRepeat(True)
        NewSongWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(NewSongWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1900, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuConfiguracion = QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(u"menuConfiguracion")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        NewSongWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(NewSongWindow)
        self.statusbar.setObjectName(u"statusbar")
        NewSongWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuConfiguracion.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(NewSongWindow)

        QMetaObject.connectSlotsByName(NewSongWindow)
    # setupUi

    def retranslateUi(self, NewSongWindow):
        NewSongWindow.setWindowTitle(QCoreApplication.translate("NewSongWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("NewSongWindow", u"Add a new song", None))
        self.image_label.setText(QCoreApplication.translate("NewSongWindow", u"TextLabel", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("NewSongWindow", u"Archivo", None))
        self.menuConfiguracion.setTitle(QCoreApplication.translate("NewSongWindow", u"Configuracion", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("NewSongWindow", u"Ayuda", None))
    # retranslateUi

