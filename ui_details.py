# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detailsgVlqmH.ui'
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

class Ui_DetailsWindow(object):
    def setupUi(self, DetailsWindow):
        if not DetailsWindow.objectName():
            DetailsWindow.setObjectName(u"DetailsWindow")
        DetailsWindow.resize(1900, 1010)
        self.centralwidget = QWidget(DetailsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 1900, 981))
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
        self.play_pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.play_pushButton.setObjectName(u"play_pushButton")
        self.play_pushButton.setGeometry(QRect(110, 420, 321, 121))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        font.setBold(True)
        self.play_pushButton.setFont(font)
        self.play_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.play_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.play_pushButton.setText(u"Play")
        self.play_pushButton.setIconSize(QSize(80, 80))
        self.play_pushButton.setAutoRepeat(True)
        self.image_label = QLabel(self.scrollAreaWidgetContents)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(100, 50, 351, 351))
        self.details_frame = QFrame(self.scrollAreaWidgetContents)
        self.details_frame.setObjectName(u"details_frame")
        self.details_frame.setGeometry(QRect(520, 70, 901, 461))
        self.details_frame.setMinimumSize(QSize(0, 0))
        self.details_frame.setMaximumSize(QSize(1000, 1000))
        self.details_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.details_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.details_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.versions_frame = QFrame(self.scrollAreaWidgetContents)
        self.versions_frame.setObjectName(u"versions_frame")
        self.versions_frame.setGeometry(QRect(110, 580, 1311, 260))
        self.versions_frame.setMinimumSize(QSize(0, 0))
        self.versions_frame.setMaximumSize(QSize(1374, 300))
        self.versions_frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.versions_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.versions_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.back_pushButton = QPushButton(self.centralwidget)
        self.back_pushButton.setObjectName(u"back_pushButton")
        self.back_pushButton.setGeometry(QRect(20, 870, 181, 81))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.back_pushButton.setFont(font1)
        self.back_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.back_pushButton.setText(u"Back")
        self.back_pushButton.setIconSize(QSize(80, 80))
        self.back_pushButton.setAutoRepeat(True)
        DetailsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(DetailsWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1900, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuConfiguracion = QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(u"menuConfiguracion")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        DetailsWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(DetailsWindow)
        self.statusbar.setObjectName(u"statusbar")
        DetailsWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuConfiguracion.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(DetailsWindow)

        QMetaObject.connectSlotsByName(DetailsWindow)
    # setupUi

    def retranslateUi(self, DetailsWindow):
        DetailsWindow.setWindowTitle(QCoreApplication.translate("DetailsWindow", u"MainWindow", None))
        self.label.setText("")
        self.image_label.setText(QCoreApplication.translate("DetailsWindow", u"imagen", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("DetailsWindow", u"Archivo", None))
        self.menuConfiguracion.setTitle(QCoreApplication.translate("DetailsWindow", u"Configuracion", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("DetailsWindow", u"Ayuda", None))
    # retranslateUi

