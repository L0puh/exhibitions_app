import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
            QVBoxLayout, QWidget, QLineEdit, 
            QGridLayout, QTextEdit, QLabel,
            QComboBox, QPushButton, QMessageBox, 
            QHBoxLayout, QDateTimeEdit
        )

from src.data import *

class Exhibit_widget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.owners = ["OWNER 1", "OWNER 2"] #FIXME 
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Экспонат")
    
       
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название")

        self.owner_label = QLabel("\tВладелец:")
        self.owner_input = QComboBox(self)
        self.owner_input.addItems(self.owners)
        
        
        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_exhibit)
        self.save_btn.setFixedSize(self.save_btn.sizeHint())

        
        layout = QHBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.owner_label)
        layout.addWidget(self.owner_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_exhibit(self):
        name = self.name_input.text()
        owner = self.owner_input.currentText()
        if name and owner:
            e = Exhibit(name, owner)
            QMessageBox.information(self, "", f"{name} добавлен")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка добавления", "Заполните все поля") 
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class Exhibition_widget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выставка")
    
       
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название")

        self.about_input = QTextEdit()
        self.about_input.setFixedHeight(500)
        self.about_input.setPlaceholderText("Описание...")

        
        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_exhibition)
        self.save_btn.setFixedSize(self.save_btn.sizeHint())
        
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.about_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_exhibition(self):
        name = self.name_input.text()
        about = self.about_input.toPlainText()
        if name and about:
            e = Exhibition(name, about) 
            QMessageBox.information(self, "", f"{name} добавлен")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка добавления", "Заполните все поля") 
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class Order_hold_widget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.exhibits    = Exhibit.get_exhibits()
        self.exhibitions = Exhibition.get_exhibtions()
        self.places      = ["PLACE 1", "PLACE 2"] #FIXME
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приказ")
        
        reglabel = QLabel("Дата формирования приказа: ")
        self.datereg = QDateTimeEdit()
        self.datereg.setDateTime(datetime.datetime.now())
        self.datereg.setDisplayFormat("dd/MM/yy HH:MM")
        self.datereg.setCalendarPopup(1)

        exhibtion_label = QLabel("Выберите выставку: ")
        self.exhibition_input = QComboBox(self)
        self.exhibition_input.addItems(self.exhibitions)
        
        dates_label = QLabel("Выберите даты проведения: ")
        # TODO: self.dates = []
        
        place_label = QLabel("Выберите место: ")
        self.place_input = QComboBox(self)
        self.place_input.addItems(self.places)

        exhibits_label = QLabel("Выберите экспонаты: ")
        self.exhibits_input = QComboBox(self)
        self.exhibits_input.addItems(self.exhibits)

        self.save_btn = QPushButton("Сохранить")
        
        layout = QVBoxLayout()
        layout.addWidget(reglabel)
        layout.addWidget(self.datereg)
        layout.addWidget(exhibtion_label)
        layout.addWidget(self.exhibition_input)
        layout.addWidget(dates_label)
        layout.addWidget(place_label)
        layout.addWidget(self.place_input)
        layout.addWidget(exhibits_label)
        layout.addWidget(self.exhibits_input)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

