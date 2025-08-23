from PySide6.QtWidgets import QApplication
from ui.homewindow import HomeWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())