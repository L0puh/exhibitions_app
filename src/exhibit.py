class Exhibit:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

class Exhibition:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Order_hold:
    def __init__(self, date_reg, date_hold, exhibition:Exhibition, place, exhibits):
        self.date_reg = date_reg
        self.date_hold = date_hold
        self.exhibition = exhibition
        self.place = place
        self.exhibits = exhibits
