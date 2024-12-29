import datetime

from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtWidgets import (
            QVBoxLayout, QWidget, QLineEdit, 
            QGridLayout, QTextEdit, QLabel,
            QComboBox, QPushButton, QMessageBox, 
            QHBoxLayout, QDateTimeEdit, QTableWidget,
            QTableWidgetItem, QListWidget
        )

from PyQt6.QtGui import QIcon


from src.data import *
from src.common import *

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
        
        self.data_exhibits = [i["input"] for i in self.exhibits]
        self.exhibitions_data = [i["name"] for i in self.exhibitions]

        self.chosen_exhibits = []
        self.dates = []
        self.datetimes = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приказ")
        
        reglabel = QLabel("Дата формирования приказа: ")
        self.datereg = QDateTimeEdit()
        self.datereg.setDateTime(QDateTime.currentDateTime())
        self.datereg.setDisplayFormat("dd/MM/yy HH:MM")
        self.datereg.setCalendarPopup(1)

        exhibtion_label = QLabel("Выберите выставку: ")
        self.exhibition_input = QComboBox(self)
        self.exhibition_input.addItems(self.exhibitions_data)
        
        dates_label = QLabel("Выберите даты проведения: ")
        self.date= QDateTimeEdit()
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.date.setCalendarPopup(1)

        self.date_add = QPushButton()
        self.date_add.setIcon(QIcon(icon("add.png")))
        self.date_add.setIconSize(self.date_add.sizeHint())
        self.date_add.setFixedSize(self.date_add.sizeHint())
        self.date_add.clicked.connect(self.add_date)

        self.dates_table = QTableWidget()
        self.exhibits_table = QTableWidget()
        
        place_label = QLabel("Выберите место: ")
        self.place_input = QComboBox(self)
        self.place_input.addItems(self.places)

        self.exhibits_label = QLabel("Выберите экспонаты: ")
        self.exhibits_input = QListWidget(self)
        self.exhibits_input.addItems(self.data_exhibits)
        self.exhibits_input.clicked.connect(self.add_exhibit)
        self.exhibits_input.setFixedSize(self.exhibits_input.sizeHint())

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_order)
        
        layout = QVBoxLayout()
        layout.addWidget(reglabel)
        layout.addWidget(self.datereg)
        layout.addWidget(exhibtion_label)
        layout.addWidget(self.exhibition_input)
        layout.addWidget(dates_label)
        layout.addWidget(self.date)
        layout.addWidget(self.dates_table)
        layout.addWidget(self.date_add)
        layout.addWidget(place_label)
        layout.addWidget(self.place_input)
        layout.addWidget(self.exhibits_label)
        layout.addWidget(self.exhibits_input)
        layout.addWidget(self.exhibits_table)
        layout.addWidget(self.save_btn)
         
        self.setLayout(layout)
        self.update_dates_table()
        self.update_exhibits_table()

    def save_order(self):
        date_reg = self.datereg.dateTime()
        if date_reg.date() < datetime.datetime.now().date():
            QMessageBox.warning(self, "ОШИБКА", "Дата регистрации введена неверно")
            return

        date_reg = date_reg.toString("dd/MM/yyyy HH:mm")
        exhibition = {}
        for ex in self.exhibitions:
            if self.exhibition_input.currentText() == ex["name"]:
                exhibition = ex
                break
        place = self.place_input.currentText().strip()
        if self.chosen_exhibits and self.datetimes and exhibition:
            order = Order_hold(date_reg, self.datetimes, exhibition, place, self.chosen_exhibits)
            QMessageBox.information(self, "", f"Заказ оформлен успешно")
            self.close()

        else:
            QMessageBox.warning(self, "Ошибка", "Данные введены неверно")



    def add_exhibit(self, indx):
        exhibit = self.exhibits_input.itemFromIndex(indx).text()
        if exhibit:
            for i, ex in enumerate(self.exhibits):
                if exhibit == ex["input"]:
                    self.exhibits.pop(i)
                    self.data_exhibits.pop(i)
                    self.exhibits_input.clear()
                    self.exhibits_input.addItems(self.data_exhibits)
                    self.exhibits_input.setFixedSize(self.exhibits_input.sizeHint())
                    self.chosen_exhibits.append(ex)
                    break
        if len(self.exhibits) == 0: 
            self.exhibits_label.setText("Список экспонатов пуст")
            self.exhibits_input.hide()
        self.update_exhibits_table()
        

    def add_date(self):
        time = self.date.dateTime()
        now = datetime.datetime.now()
        if time.date() < now:
            QMessageBox.warning(self, "ОШИБКА", "Дата введена неверно")
            return
        self.datetimes.append(time.toString("dd/MM/yyyy HH:mm"))
        self.dates.append({"date": time.toString('dd/MM/yyyy'),
                           "time": time.toString('HH:mm')})
        self.dates_table.hide()
        self.update_dates_table()
   
    def update_exhibits_table(self):
        self.exhibits_table.clear()
        if self.chosen_exhibits:
            self.exhibits_table.setColumnCount(2)
            self.exhibits_table.setHorizontalHeaderLabels(["Экспонат", "Владелец"])
            self.exhibits_table.setRowCount(len(self.chosen_exhibits))
            self.exhibits_table.show()
            for row, ex in enumerate(self.chosen_exhibits):
                d = QTableWidgetItem(ex["name"])
                t = QTableWidgetItem(ex["owner"])

                for i in [t, d]:
                    i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.exhibits_table.setItem(row, 0, d)
                self.exhibits_table.setItem(row, 1, t)

            self.exhibits_table.setFixedSize(self.exhibits_table.sizeHint())

        else:
            self.exhibits_table.hide()
    
    def update_dates_table(self):
        self.dates_table.clear()
        if self.dates:
            self.dates_table.setColumnCount(2)
            self.dates_table.setHorizontalHeaderLabels(["Дата", "Время"])
            self.dates_table.setRowCount(len(self.dates))
            self.dates_table.show()
            for row, date in enumerate(self.dates):
                d = QTableWidgetItem(date["date"])
                t = QTableWidgetItem(date["time"])

                for i in [t, d]:
                    i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.dates_table.setItem(row, 0, d)
                self.dates_table.setItem(row, 1, t)
            self.dates_table.setFixedSize(self.dates_table.sizeHint())

        else:
            self.dates_table.hide()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


