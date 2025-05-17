from PySide6.QtWidgets import QApplication
from homewindow import HomeWindow
import sys

app = QApplication(sys.argv)
window = HomeWindow()
window.show()

sys.exit(app.exec_())