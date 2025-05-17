from ui_details import *
import homewindow
import videowindow

#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class DetailsWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_DetailsWindow()
        self.ui.setupUi(self)

        self.ui.back_pushButton.clicked.connect(self.home)
        self.ui.play_pushButton.clicked.connect(self.video)

    @Slot( )
    def home(self):
        global new
        new = homewindow.HomeWindow()
        new.show()
        self.hide()

    @Slot( )
    def video(self):
        global vid
        vid = videowindow.VideoWindow()
        vid.show()
        self.hide()