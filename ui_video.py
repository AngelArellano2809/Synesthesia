# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videopYOdHs.ui'
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
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_VideoWindow(object):
    def setupUi(self, VideoWindow):
        if not VideoWindow.objectName():
            VideoWindow.setObjectName(u"VideoWindow")
        VideoWindow.resize(1900, 1010)
        self.centralwidget = QWidget(VideoWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1900, 981))
        self.label.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.721889, y1:0.211, x2:0.917, y2:0.772591, stop:0.0111111 rgba(56, 56, 56, 255), stop:0.744444 rgba(95, 95, 95, 255));")
        self.home_pushButton = QPushButton(self.centralwidget)
        self.home_pushButton.setObjectName(u"home_pushButton")
        self.home_pushButton.setGeometry(QRect(30, 830, 231, 111))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(30)
        font.setBold(True)
        self.home_pushButton.setFont(font)
        self.home_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.home_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.home_pushButton.setText(u"Home")
        self.home_pushButton.setIconSize(QSize(80, 80))
        self.home_pushButton.setAutoRepeat(True)
        self.details_pushButton = QPushButton(self.centralwidget)
        self.details_pushButton.setObjectName(u"details_pushButton")
        self.details_pushButton.setGeometry(QRect(310, 830, 231, 111))
        self.details_pushButton.setFont(font)
        self.details_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.details_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.details_pushButton.setText(u"Details")
        self.details_pushButton.setIconSize(QSize(80, 80))
        self.details_pushButton.setAutoRepeat(True)
        self.video_frame = QFrame(self.centralwidget)
        self.video_frame.setObjectName(u"video_frame")
        self.video_frame.setGeometry(QRect(30, 30, 1841, 791))
        self.video_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.video_frame.setFrameShadow(QFrame.Shadow.Raised)
        VideoWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(VideoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1900, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuConfiguracion = QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(u"menuConfiguracion")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        VideoWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(VideoWindow)
        self.statusbar.setObjectName(u"statusbar")
        VideoWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuConfiguracion.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(VideoWindow)

        QMetaObject.connectSlotsByName(VideoWindow)
    # setupUi

    def retranslateUi(self, VideoWindow):
        VideoWindow.setWindowTitle(QCoreApplication.translate("VideoWindow", u"MainWindow", None))
        self.label.setText("")
        self.menuArchivo.setTitle(QCoreApplication.translate("VideoWindow", u"Archivo", None))
        self.menuConfiguracion.setTitle(QCoreApplication.translate("VideoWindow", u"Configuracion", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("VideoWindow", u"Ayuda", None))
    # retranslateUi

