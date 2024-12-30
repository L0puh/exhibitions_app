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

        self.owner_label = QLabel("Владелец:")
        self.owner_input = QComboBox(self)
        self.owner_input.addItems(self.owners)
        
        
        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_exhibit)
        self.save_btn.setFixedSize(self.save_btn.sizeHint())

        
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.owner_label)
        layout.addWidget(self.owner_input)
        layout.addWidget(self.save_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
         
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
            self.exhibits_table.setColumnCount(3)
            self.exhibits_table.setHorizontalHeaderLabels(["Экспонат", "Владелец", "Статус"])
            self.exhibits_table.setRowCount(len(self.chosen_exhibits))
            self.exhibits_table.show()
            for row, ex in enumerate(self.chosen_exhibits):
                d = QTableWidgetItem(ex["name"])
                t = QTableWidgetItem(ex["owner"])
                s = Exhibit.get_status(ex["status"])
                if ex["status"] == 2:
                    QMessageBox.information(self, "", f"{ex['name']} уже забронировн\nДанный экспонат не будет учитываться\
                                                                                        до момент измнения статуса")

                s = QTableWidgetItem(s)
                for i in [t, d, s]:
                    i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.exhibits_table.setItem(row, 0, d)
                self.exhibits_table.setItem(row, 1, t)
                self.exhibits_table.setItem(row, 2, s)


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

class Order_base:
    def initUI(widget, date_label, is_give=0, is_return=0):
        widget.setWindowTitle("Приказ")

        date_label = QLabel(date_label)
        widget.date = QDateTimeEdit()
        widget.date.setDateTime(QDateTime.currentDateTime())
        widget.date.setDisplayFormat("dd/MM/yyyy HH:mm")
        widget.date.setCalendarPopup(1)

        widget.order_label = QLabel("Выберите приказ о проведении выставки:")
        widget.order_input = QListWidget()
        widget.order_input.addItems(widget.orders_data)
        widget.order_input.clicked.connect(lambda i: Order_base.fetch_exhibits(widget,i, is_give=is_give, is_return=is_return))

        widget.exhibits_label = QLabel("Выберите приказ для отображения экспонатов")

        widget.exhibits_input = QListWidget(widget)
        widget.exhibits_input.clicked.connect(lambda i: Order_base.add_exhibits_table(widget, i, is_give=is_give, is_return=is_return))
        widget.exhibits_input.setFixedSize(widget.exhibits_input.sizeHint())
        
        widget.exhibits_input.hide()
        widget.save_btn = QPushButton("Сохранить")
        widget.save_btn.clicked.connect(lambda: Order_base.save_order(widget, is_give=is_give, is_return=is_return))

        widget.exhibits_table = QTableWidget()
        widget.exhibits_table.hide()

        layout = QVBoxLayout()
        layout.addWidget(date_label)
        layout.addWidget(widget.date)
        layout.addWidget(widget.order_label)
        layout.addWidget(widget.order_input)
        layout.addWidget(widget.exhibits_label)
        layout.addWidget(widget.exhibits_input)
        layout.addWidget(widget.exhibits_table)
        layout.addWidget(widget.save_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(layout)
        
        if widget.order_id != -1:
            widget.order_input.hide()
            Order_base.fetch_exhibits(widget, -1, is_return=is_return, is_give=is_give)
        return widget

    def add_exhibits_table(widget, indx, is_give=0, is_return=0):
        exhibit = widget.exhibits_input.itemFromIndex(indx).text()
        if exhibit:
            for i, ex in enumerate(widget.exhibits):
                if exhibit == ex["input"]:
                    widget.exhibits.pop(i)
                    widget.data_exhibits.pop(i)
                    widget.exhibits_input.clear()
                    widget.exhibits_input.addItems(widget.data_exhibits)
                    widget.exhibits_input.setFixedSize(widget.exhibits_input.sizeHint())
                    widget.chosen_exhibits.append(ex)
                    break

        if len(widget.exhibits) == 0: 
            widget.exhibits_label.setText("Список экспонатов пуст")
            widget.exhibits_input.hide()

        Order_base.update_exhibits_table(widget, is_give=is_give, is_return=is_return)

    def fetch_exhibits(widget, indx, is_return=0, is_give=0):
        if indx != -1:
            item = widget.order_input.itemFromIndex(indx).text()
            cur_order = {}
            for i, order in enumerate(widget.orders):
                if order["input"] == item:
                    cur_order = order
                    widget.order_id = order["id"]
                    break
        else:
            cur_order = widget.order
        if is_return:
            widget.exhibits = Order_hold.get_exhibits_rented_out(cur_order["id"])
        elif is_give:
            widget.exhibits = Order_hold.get_exhibits_ready_rentout(cur_order["id"])
        else:
            widget.exhibits = Order_hold.get_exhibits(cur_order["id"])
        widget.data_exhibits = [i["input"] for i in widget.exhibits]
        widget.exhibits_input.addItems(widget.data_exhibits)
        widget.exhibits_label.setText("Выберите экспонаты: ")
        widget.exhibits_input.show()
        widget.order_label.setText(f"Приказ выбран: {cur_order['input']}")
        widget.order_input.hide()
        if len(widget.exhibits) == 0: 
            if is_give:
                QMessageBox.information(widget, "", "Список экспонатов готовых для бронирования пуст")
            elif is_return:
                QMessageBox.information(widget, "", "Список экспонатов готовых для возврата пуст")
            else:
                QMessageBox.information(widget, "", "Список экспонатов готовых для передачи пуст")
            widget.close()
        return widget 


    def update_exhibits_table(widget, is_give=0, is_return=0):
        widget.exhibits_table.clear()
        if widget.chosen_exhibits:
            widget.exhibits_table.setColumnCount(3)
            widget.exhibits_table.setHorizontalHeaderLabels(["Экспонат", "Владелец", "Статус"])
            widget.exhibits_table.setRowCount(len(widget.chosen_exhibits))
            widget.exhibits_table.show()
            for row, ex in enumerate(widget.chosen_exhibits):
                d = QTableWidgetItem(ex["name"])
                t = QTableWidgetItem(ex["owner"])

                s = QTableWidgetItem(Exhibit.get_status(ex["status"]))
                if ex["status"] == 2 and not is_return:
                    QMessageBox.information(widget, "", f"{ex['name']} уже забронировн\nДанный экспонат не будет учитываться\
                                                                                        до момент измнения статуса")
                for i in [t, d,s ]:
                    i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)

                widget.exhibits_table.setItem(row, 0, d)
                widget.exhibits_table.setItem(row, 1, t)
                widget.exhibits_table.setItem(row, 2, s)

        else:
            widget.exhibits_table.hide()
        return widget 

    def save_order(widget, is_give=0, is_return=0):
        date = widget.date.dateTime()
        if date.date() < datetime.datetime.now().date():
            QMessageBox.warning(widget, "ОШИБКА", "Дата введена неверно")
            return

        date = date.toString("dd/MM/yyyy HH:mm")
        
        if widget.chosen_exhibits:
            if is_give:
                order = Order_give(date, widget.order_id, widget.chosen_exhibits)
            elif is_return:
                order = Order_return(date, widget.order_id, widget.chosen_exhibits)
            else:
                order = Order_get(date, widget.order_id, widget.chosen_exhibits)
            QMessageBox.information(widget, "", f"Заказ оформлен успешно")
            widget.close()

        else:
            QMessageBox.warning(widget, "Ошибка", "Данные введены неверно")

class Order_get_widget(QWidget):
    def __init__(self, window, data):
        super().__init__()
        self.window = window
        self.orders = Order_hold.get_orders()
        self.orders_data = [i["input"] for i in self.orders] if self.orders else []
        self.chosen_exhibits = []
        self.data_exhibits = []
        self.exhibits = []
        
        self.order_id = -1 if not data else data["id"]
        self.order = data

        self = Order_base.initUI(self, "Выберите дату поступления: ")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class Order_give_widget(QWidget):
    def __init__(self, window, data):
        super().__init__()
        self.window = window
        self.orders = Order_get.get_hold_orders()
        self.orders_data = [i["input"] for i in self.orders] if self.orders else []
        self.exhibits = []
        self.exhibits_data = []
        self.chosen_exhibits = []
        self.order_id = -1 if not data else data["id"]
        self.order = data
        self = Order_base.initUI(self, "Выберите дату передачи экспонатов:",is_give=1)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class Order_return_widget(QWidget):
    def __init__(self, window, data):
        super().__init__()
        self.window = window
        self.orders = Order_give.get_get_orders()
        self.orders_data = [i["input"] for i in self.orders] if self.orders else []
        self.exhibits = []
        self.exhibits_data = []
        self.chosen_exhibits = []
        self.order_id = -1 if not data else data["id"]
        self.order = data
        self = Order_base.initUI(self, "Выберите дату возврата: ", is_return=1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

class Orders_list_widget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Список")
        self.setGeometry(600, 600, 500, 500)
        self.list_orders = QListWidget()
        self.update_list()

        layout = QVBoxLayout()
        layout.addWidget(self.list_orders)
        self.setLayout(layout)
   
    def update_list(self):
        self.orders = Order_hold.get_orders()
        self.list_orders.clear()
        self.orders_data = [i["input"] for i in self.orders] if self.orders else []
        
        for indx, data in enumerate(self.orders):
            item = QListWidgetItem()
            name_label = QLabel(data["input"])
            status_label = QLabel(f"Статус: {Order_hold.get_status(data['status'])}")

            button = QPushButton()
            get_icon = QIcon(icon("get.png"))
            give_icon = QIcon(icon("give.png"))
            return_icon = QIcon(icon("return.png"))
            delete_icon = QIcon(icon("delete.png"))

            if data["status"] == 0:
                button.setIcon(get_icon)
                button.clicked.connect(lambda: self.open_order_get(indx))
            elif data["status"] == 1:
                button.setIcon(give_icon)
                button.clicked.connect(lambda: self.open_order_give(indx))
            elif data["status"] == 2:
                button.setIcon(return_icon)
                button.clicked.connect(lambda: self.open_order_return(indx))
            else:
                button.setIcon(delete_icon)
                button.clicked.connect(lambda: self.delete_order(indx))

            button.setIconSize(button.sizeHint())
            button.setFixedSize(button.iconSize())

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(status_label)
            layout.addWidget(button)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.list_orders.addItem(item)
            self.list_orders.setItemWidget(item, widget)
       
    def open_order_get(self, indx):
        self.window.open_order_get(self.orders[indx])
        self.close()

    def open_order_give(self, indx):
        self.window.open_order_give(self.orders[indx])
        self.close()

    def open_order_return(self, indx):
        self.window.open_order_return(self.orders[indx])
        self.close()

    def delete_order(self, indx):
        Order_hold.delete_order(self.orders[indx]["id"])
        self.update_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
