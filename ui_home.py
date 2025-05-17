# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_templateBmlufg.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        if not HomeWindow.objectName():
            HomeWindow.setObjectName(u"HomeWindow")
        HomeWindow.resize(1900, 1010)
        self.centralwidget = QWidget(HomeWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 1900, 981))
        self.label.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.721889, y1:0.211, x2:0.917, y2:0.772591, stop:0.0111111 rgba(56, 56, 56, 255), stop:0.744444 rgba(95, 95, 95, 255));")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(429, 180, 1044, 770))
        self.scrollArea.setMinimumSize(QSize(1044, 770))
        self.scrollArea.setMaximumSize(QSize(16777215, 770))
        self.scrollArea.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgba(122, 122, 122, 50%);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1032, 814))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.search_lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.search_lineEdit.setObjectName(u"search_lineEdit")
        self.search_lineEdit.setMinimumSize(QSize(455, 40))
        self.search_lineEdit.setMaximumSize(QSize(455, 40))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(16)
        self.search_lineEdit.setFont(font)
        self.search_lineEdit.setStyleSheet(u"border-radius: 20px;\n"
"background-color: rgb(192, 192, 192);")

        self.verticalLayout.addWidget(self.search_lineEdit, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(901, 246))
        self.frame_2.setMaximumSize(QSize(901, 246))
        self.frame_2.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(901, 246))
        self.frame_3.setMaximumSize(QSize(901, 246))
        self.frame_3.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(901, 246))
        self.frame.setMaximumSize(QSize(901, 246))
        self.frame.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(192, 192, 192);\n"
"border-width: 5;\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.add_pushButton = QPushButton(self.centralwidget)
        self.add_pushButton.setObjectName(u"add_pushButton")
        self.add_pushButton.setGeometry(QRect(448, 20, 483, 135))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(36)
        font1.setBold(True)
        self.add_pushButton.setFont(font1)
        self.add_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.add_pushButton.setText(u"Add")
        self.add_pushButton.setIconSize(QSize(80, 80))
        self.add_pushButton.setAutoRepeat(True)
        self.playlist_pushButton = QPushButton(self.centralwidget)
        self.playlist_pushButton.setObjectName(u"playlist_pushButton")
        self.playlist_pushButton.setGeometry(QRect(970, 20, 483, 135))
        self.playlist_pushButton.setFont(font1)
        self.playlist_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.playlist_pushButton.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:0.028, x2:1, y2:0.579, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(32, 32, 32, 255));\n"
"border-radius: 30px;")
        self.playlist_pushButton.setText(u"Playlist")
        self.playlist_pushButton.setIconSize(QSize(80, 80))
        self.playlist_pushButton.setAutoRepeat(True)
        HomeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(HomeWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1900, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuConfiguracion = QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(u"menuConfiguracion")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        HomeWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(HomeWindow)
        self.statusbar.setObjectName(u"statusbar")
        HomeWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuConfiguracion.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(HomeWindow)

        QMetaObject.connectSlotsByName(HomeWindow)
    # setupUi

    def retranslateUi(self, HomeWindow):
        HomeWindow.setWindowTitle(QCoreApplication.translate("HomeWindow", u"MainWindow", None))
        self.label.setText("")
        self.search_lineEdit.setPlaceholderText(QCoreApplication.translate("HomeWindow", u"   Search", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("HomeWindow", u"Archivo", None))
        self.menuConfiguracion.setTitle(QCoreApplication.translate("HomeWindow", u"Configuracion", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("HomeWindow", u"Ayuda", None))
    # retranslateUi

