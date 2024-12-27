from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget

class Window(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Главное")
        self.setGeometry(800, 800, 800, 800)

        self.central = QWidget(self)
        
        layout = QHBoxLayout()
        self.central.setLayout(layout)
        self.setCentralWidget(self.central)
        self.statusBar = self.statusBar()





