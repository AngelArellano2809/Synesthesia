from ui.ui_home import *
import ui.newsongwindow
import ui.videowindow

#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class HomeWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)

        self.ui.add_pushButton.clicked.connect(self.newSong)
        self.ui.playlist_pushButton.clicked.connect(self.video)

    @Slot( )
    def newSong(self):
        global new
        new = ui.newsongwindow.NewSongWindow()
        new.show()
        self.hide()

    @Slot( )
    def video(self):
        global vid
        vid = ui.videowindow.VideoWindow()
        vid.show()
        self.hide()

