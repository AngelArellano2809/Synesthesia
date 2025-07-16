from ui.ui_new_song import *
import ui.homewindow

#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class NewSongWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_NewSongWindow()
        self.ui.setupUi(self)

        self.ui.back_pushButton.clicked.connect(self.home)

    @Slot( )
    def home(self):
        global new
        new = ui.homewindow.HomeWindow()
        new.show()
        self.hide()