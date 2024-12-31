import datetime

from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtWidgets import (
            QVBoxLayout, QWidget, QLineEdit, 
            QGridLayout, QTextEdit, QLabel,
            QComboBox, QPushButton, QMessageBox, 
            QHBoxLayout, QDateTimeEdit, QTableWidget,
            QTableWidgetItem, QListWidget, QListWidgetItem
        )

from PyQt6.QtGui import QIcon

from src.data import *
from src.common import *

def initUI(widget):
    widget.setWindowTitle("Список")
    widget.setGeometry(800, 800, 800, 800)

    widget.list = QListWidget()
    
    layout = QVBoxLayout()
    layout.addWidget(widget.list)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    widget.setLayout(layout)
    return widget


class Exhibits_list_widget(QWidget):
    def __init__(self):
        super().__init__()
        self = initUI(self)
        self.update_list()

    def update_list(self):
        self.list.clear()
        self.exhibits = Exhibit.get_exhibits()
        
        for indx, data in enumerate(self.exhibits):
            item = QListWidgetItem()
            name_label = QLabel(data["name"])
            owner_label = QLabel(f'Владелец: {data["owner"]}')
            status_label = QLabel(f"Статус: {Exhibit.get_status(data['status'])}")

            for label in [owner_label, status_label, name_label]:
                label.setWordWrap(1)
                label.setFixedWidth(200)

            
            button = QPushButton()
            delete_icon = QIcon(icon("delete.png"))
            button.setIcon(delete_icon)
            button.clicked.connect(lambda: self.delete_exhibit(indx))
            
            button.setIconSize(button.sizeHint())
            button.setFixedSize(button.iconSize())

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(owner_label)
            layout.addWidget(status_label)
            layout.addWidget(button)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

    def delete_exhibit(self, indx):
        Exhibit.delete_exhibit(self.exhibits[indx]["id"])
        self.update_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        
class Exhibitions_list_widget(QWidget):
    def __init__(self):
        super().__init__()
        self = initUI(self)
        self.update_list()
   
    def update_list(self):
        self.list.clear()
        self.exhibitions = Exhibition.get_exhibtions()
        
        for indx, data in enumerate(self.exhibitions):
            item = QListWidgetItem()
            name_label = QLabel(data["name"])
            sz = len(data["about"])//2
            orders_cnt = len(Exhibition.get_connected_orders(data["id"]))
            orders_cnt_label = QLabel(f"Количество орагнизаций: {orders_cnt}")
            about_label = QLabel(f'{data["about"][:sz if sz < 100 else 100]}...')
            
            for label in [name_label, about_label, orders_cnt_label]:
                label.setWordWrap(1)
                label.setFixedWidth(200)

            button = QPushButton()
            show_btn = QPushButton()
            show_icon = QIcon(icon("about.png"))
            delete_icon = QIcon(icon("delete.png"))

            show_btn.setIcon(show_icon)
            show_btn.clicked.connect(lambda: self.show_exhibition(indx))
            button.setIcon(delete_icon)
            button.clicked.connect(lambda: self.delete_exhibition(indx))
            
            button.setIconSize(button.sizeHint())
            button.setFixedSize(button.iconSize())
            
            show_btn.setIconSize(show_btn.sizeHint())
            show_btn.setFixedSize(show_btn.iconSize())

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(about_label)
            layout.addWidget(orders_cnt_label)
            layout.addWidget(show_btn)
            layout.addWidget(button)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)
        
    def show_exhibition(self, indx):
        QMessageBox.information(self, "", self.exhibitions[indx]["name"] + "\n" + self.exhibitions[indx]["about"])

    def delete_exhibition(self, indx):
        Exhibition.delete_exhibition(self.exhibitions[indx]["id"])
        self.update_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        
