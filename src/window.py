from src.widgets import *


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QAction, QIcon

from src.common import WELCOME_TEXT
from src.lists_widget import *

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Главное")
        self.setGeometry(800, 800, 800, 800)

        self.central = QWidget(self)
        self.draw_menu()
        
        welcome_label = QLabel(WELCOME_TEXT)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        order_btn = QPushButton()
        order_btn.setText("Создать приказ о проведении")
        orders_btn = QPushButton() 
        orders_btn.setText("Открыть список всех приказов")
        
        order_btn.clicked.connect(self.open_order_hold)
        orders_btn.clicked.connect(self.open_orders_list)

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(order_btn)
        btn_layout.addWidget(orders_btn)
        layout.addWidget(welcome_label)
        layout.addLayout(btn_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.central.setLayout(layout)
        self.setCentralWidget(self.central)
        self.statusBar = self.statusBar()

    def draw_menu(self):
        menu_bar = self.menuBar()

        m_main = menu_bar.addMenu("&Меню")
        m_orders = menu_bar.addMenu("&Приказы")
        m_lists = menu_bar.addMenu("&Данные")
        m_help = menu_bar.addMenu("&Помощь")

        a_exit = QAction(QIcon(icon("exit.png")), "&Выход", self)
        a_exit.setShortcut("Esc")
        a_exit.triggered.connect(self.close)

        a_exhibit = QAction(QIcon(icon("add.png")), "&Добавить экспонат", self)
        a_exhibit.triggered.connect(self.open_exhibit_widget)

        a_exhibition = QAction(QIcon(icon("add.png")), "&Добавить выставку", self)
        a_exhibition.triggered.connect(self.open_exhibition_widget)

        a_order_hold = QAction(QIcon(icon("order.png")), "&Приказ о проведении", self)
        a_order_hold.triggered.connect(self.open_order_hold)

        a_orders_list = QAction(QIcon(icon("list.png")), "&Список приказов", self)
        a_orders_list.triggered.connect(self.open_orders_list)
        
        a_exhibits_list = QAction(QIcon(icon("list.png")), "&Список экспонатов", self)
        a_exhibits_list.triggered.connect(self.open_exhibits_list)

        a_exhibitions_list = QAction(QIcon(icon("list.png")), "&Список выставок", self)
        a_exhibitions_list.triggered.connect(self.open_exhibitions_list)

        m_main.addAction(a_exhibit)
        m_main.addAction(a_exhibition)
        m_main.addAction(a_exit)
        
        m_lists.addAction(a_exhibits_list)
        m_lists.addAction(a_exhibitions_list)
        m_orders.addAction(a_order_hold)
        m_orders.addAction(a_orders_list)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def open_exhibit_widget(self):
        self.exhibit = Exhibit_widget(self)
        self.exhibit.show()
    
    def open_exhibition_widget(self):
        self.exhibition = Exhibition_widget(self)
        self.exhibition.show()
    
    def open_order_hold(self):
        self.order_hold = Order_hold_widget(self)
        self.order_hold.show()
    
    def open_order_get(self, data=[]):
        self.order_get = Order_get_widget(self, data)
        self.order_get.show()
    
    def open_order_give(self, data=[]):
        self.order_give = Order_give_widget(self, data)
        self.order_give.show()
    
    def open_order_return(self, data=[]):
        self.order_return = Order_return_widget(self, data)
        self.order_return.show()

    def open_orders_list(self, data=[]):
        self.orders_list = Orders_list_widget(self)
        self.orders_list.show()

    def open_exhibits_list(self):
        self.exhibits_list = Exhibits_list_widget()
        self.exhibits_list.show()

    def open_exhibitions_list(self):
        self.exhibitions_list = Exhibitions_list_widget()
        self.exhibitions_list.show()
