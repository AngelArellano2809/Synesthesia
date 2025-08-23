from PySide6.QtWidgets import QApplication
from ui.serverwindow import ServerWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec())