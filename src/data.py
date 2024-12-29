from src.database import *

class Exhibit:
    """
    0 - open 
    1 - ready to be rented
    2 - rented
    """

    def __init__(self, name, owner):
        self.id = 0
        self.name = name
        self.owner = owner
        self.status = 0
        
        self.insert_exhibit()

    def insert_exhibit(self):
        self.id = get_last_id("exhibits", "exhibit_id")+1
        query = f'''INSERT INTO exhibits (exhibit_id, name, owner, status) 
                   VALUES(?, ?, ?, ?);'''
        
        execute_query(query, (self.id, self.name, self.owner, self.status))

    def change_status(self, new_status):
        query = f'''UPDATE exhibits SET status={new_status} WHERE exhibit_id = {self.id};'''
        execute_query(query)

    def get_exhibits():
        data = select_all("exhibits")
        names = []
        for d in data:
            names.append({"name": d[1], "owner": d[2], "id": int(d[0]), "input": f"{d[1]} ({d[2]})"})
        return names



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

    def get_exhibtions():
        data: sqlite.Row = select_all("exhibitions")
        names = []
        for d in data:
            names.append({"name": d[1], "about": d[2], "id": int(d[0])})
        return names


class Order_hold:
    def __init__(self, reg, hold:list, exhibition: dict, place, exhibits: list[dict]):
        self.id = 0
        self.reg = reg
        self.hold = hold
        self.exhibition = exhibition
        self.place = place
        self.exhibits = exhibits

        self.insert_order_to_hold()
    
    def insert_order_to_hold(self):

        query = '''INSERT INTO order_hold (order_id, date_reg, exhibition_id, place) 
                   VALUES(?, ?, ?, ?);'''
        
        self.id = get_last_id("order_hold", "order_id")+1
        execute_query(query, (self.id, self.reg, self.exhibition["id"], self.place))

        
        query = '''INSERT INTO order_hold_exhibits (order_id, exhibit_id) 
                   VALUES(?, ?);'''
      
        for ex in self.exhibits:
            execute_query(query, (self.id, ex["id"]))
        
        query = '''INSERT INTO order_hold_dates (order_id, date_hold) 
                   VALUES(?, ?);'''

        for da in self.hold:
            execute_query(query, (self.id, da))

        print("[+] order hold added:", self.id)


class Order_get:
    def __init__(self, date, order: Order_hold, exhibits: list[Exhibit]):
        self.date = date
        self.order = order
        self.exhibits = exhibits

        self.insert_order_to_get()

    def insert_order_to_get(self):
        pass


class Order_give:
    def __init__(self, date, order: Order_hold, exhibits: list[Exhibit]):
        self.date = date
        self.order = order
        self.exhibits = exhibits

        self.insert_order_to_give()

    def insert_order_to_give(self):
        pass


class Order_return:
    def __init__(self, date, order: Order_hold, exhibits: list[Exhibit]):
        self.date = date
        self.order = order
        self.exhibits = exhibits
        

        self.insert_order_to_return()

    def insert_order_to_return(self):
        pass
