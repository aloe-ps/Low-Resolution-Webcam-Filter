import sys

from ui.ui import ControlUI
from PyQt5.QtWidgets import QApplication

def start_ui(config):
    app = QApplication(sys.argv)
    from PyQt5.QtGui import QFont
    app.setFont(QFont("Segoe UI", 11))
    win = ControlUI(config)
    win.show()
    app.exec_()