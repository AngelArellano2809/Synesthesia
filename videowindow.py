from ui_video import *
import homewindow
import detailswindow

#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class VideoWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_VideoWindow()
        self.ui.setupUi(self)

        self.ui.home_pushButton.clicked.connect(self.home)
        self.ui.details_pushButton.clicked.connect(self.details)

    @Slot( )
    def home(self):
        global new
        new = homewindow.HomeWindow()
        new.show()
        self.hide()

    @Slot( )
    def details(self):
        global det
        det = detailswindow.DetailsWindow()
        det.show()
        self.hide()