import sys, datetime

from src.data import *
from src.database import *
from src.window import Window
from src.common import *

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
