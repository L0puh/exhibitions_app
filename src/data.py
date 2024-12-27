from src.database import *

class Exhibit:
    def __init__(self, name, owner):
        self.id = 0
        self.name = name
        self.owner = owner
        
        self.insert_exhibit()

    def insert_exhibit(self):
        self.id = get_last_id("exhibits", "exhibit_id")+1
        query = f'''INSERT INTO exhibits (exhibit_id, name, owner) 
                   VALUES(?, ?, ?);'''
        
        execute_query(query, (self.id, self.name, self.owner))


class Exhibition:
    def __init__(self, name, description):
        self.id = 0
        self.name = name
        self.description = description
        
        self.insert_exhibition()

    def insert_exhibition(self):
        query = f'''INSERT INTO exhibitions 
                   (exhibition_id, name, description) 
                   VALUES(?, ?, ?);'''
        
        self.id = get_last_id("exhibitions", "exhibition_id")+1
        execute_query(query, (self.id, self.name, self.description))

class Order_hold:
    def __init__(self, reg, hold, exhibition: Exhibition, place, exhibits: list):
        self.id = 0
        self.reg = reg
        self.hold = hold
        self.exhibition = exhibition
        self.place = place
        self.exhibits = exhibits

        self.insert_order_to_hold()
    
    def insert_order_to_hold(self):

        query = '''INSERT INTO order_hold (order_id, date_reg, date_hold, exhibition_id, place) 
                   VALUES(?, ?, ?, ?, ?);'''
        
        self.id = get_last_id("order_hold", "order_id")+1
        execute_query(query, (self.id, self.reg, self.hold, self.exhibition.id, self.place))
        
        query = '''INSERT INTO order_hold_exhibits (order_id, exhibit_id) 
                   VALUES(?, ?);'''
      
        for ex in self.exhibits:
            execute_query(query, (self.id, ex.id))


