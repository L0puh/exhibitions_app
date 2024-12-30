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
    widget.setGeometry(600, 600, 600, 600)

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
            owner_label = QLabel(f'{data["about"][:sz if sz < 100 else 100]}...')
            
            button = QPushButton()
            delete_icon = QIcon(icon("delete.png"))
            button.setIcon(delete_icon)
            button.clicked.connect(lambda: self.delete_exhibition(indx))
            
            button.setIconSize(button.sizeHint())
            button.setFixedSize(button.iconSize())

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(owner_label)
            layout.addWidget(button)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

    def delete_exhibition(self, indx):
        Exhibition.delete_exhibition(self.exhibitions[indx]["id"])
        self.update_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        
