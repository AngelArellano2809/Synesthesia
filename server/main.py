from PySide6.QtWidgets import QApplication
from ui.serverwindow import ServerWindow
import sys

app = QApplication(sys.argv)
window = ServerWindow()
window.show()

sys.exit(app.exec_())