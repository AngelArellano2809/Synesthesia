from ui.ui_server_window import *

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class ServerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)