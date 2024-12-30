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

    def change_status(exhibit_id, new_status):
        ex = Exhibit.get_exhibit(exhibit_id)
        query = f'''UPDATE exhibits SET status={new_status} WHERE exhibit_id = {exhibit_id};'''
        execute_query(query)

    def get_exhibits():
        data = select_all("exhibits")
        names = []
        for d in data:
            names.append({"name": d[1], "owner": d[2], "status": int(d[3]), "id": int(d[0]), 
                          "input": f"{d[1]} ({d[2]})"})
        return names

    def get_status(status):
        if status == 0: return "Не забронирован"
        if status == 1: return "Готов к брони"
        return "Забронирован"
    
    def get_exhibit(exhibit_id):
        d = select_one_where("exhibits", ["exhibit_id"], [exhibit_id])
        if d: return {"name": d[1], "owner": d[2], "status": int(d[3]), "id": int(d[0]), 
                          "input": f"{d[1]} ({d[2]})"}
        return {}
    
    def delete_exhibit(exhibit_id):
        delete_where("exhibits", "exhibit_id", exhibit_id)



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
        data: sqlite3.Row = select_all("exhibitions")
        names = []
        for d in data:
            names.append({"name": d[1], "about": d[2], "id": int(d[0])})
        return names
    
    def delete_exhibition(exhibition_id: int):
        delete_where("exhibitions", "exhibition_id", exhibition_id)


class Order_hold:
    """
    0 - none
    1 - get
    2 - give
    3 - return

    """
    def __init__(self, reg, hold:list, exhibition: dict, place, exhibits: list[dict]):
        self.id = 0
        self.reg = reg
        self.hold = hold
        self.exhibition = exhibition
        self.place = place
        self.exhibits = exhibits
        self.status = 0

        self.insert_order_to_hold()
    
    def get_status(status):
        if status == 0:
            return "Обрабатывается"
        if status == 1:
            return "Поступление экспонатов"
        if status == 2:
            return "Передача экспонатов"
        return "Возврат экспонатов"
        
    def change_status(new_status, order_id):
        order = Order_hold.get_order(order_id)
        query = f'''UPDATE order_hold SET status={new_status} WHERE order_id = {order_id};'''
        print(f"[+] ({order_id}) order status changed to {new_status}")
        execute_query(query)

    def insert_order_to_hold(self):

        query = '''INSERT INTO order_hold (order_id, date_reg, exhibition_id, place, status) 
                   VALUES(?, ?, ?, ?, ?);'''
        
        self.id = get_last_id("order_hold", "order_id")+1
        execute_query(query, (self.id, self.reg, self.exhibition["id"], self.place, self.status))

        
        query = '''INSERT INTO order_hold_exhibits (order_id, exhibit_id) 
                   VALUES(?, ?);'''
      
        for ex in self.exhibits:
            execute_query(query, (self.id, ex["id"]))
        
        query = '''INSERT INTO order_hold_dates (order_id, date_hold) 
                   VALUES(?, ?);'''

        for da in self.hold:
            execute_query(query, (self.id, da))

        print("[+] order hold added:", self.id)

    def get_exhibits(order_id) -> list:
        data = select_where("order_hold_exhibits", "order_id", order_id)
        ex = []

        for i in data:
            ex_id = int(i[1])
            d = select_one_where("exhibits", ["exhibit_id"], [ex_id])

            ex.append({"id": int(d[0]), "name": d[1], "owner": d[2], "status": int(d[3]),
                             "input": f"{d[1]} ({d[2]})"})
        return ex

    def get_exhibits_ready_rentout(order_id) -> list:
        data = select_where("order_hold_exhibits", "order_id", order_id)
        ex = []

        for i in data:
            ex_id = int(i[1])
            d = select_one_where("exhibits", ["exhibit_id", "status"], [ex_id, 1])
            if d:
                ex.append({"id": int(d[0]), "name": d[1], "owner": d[2], "status": int(d[3]),
                                 "input": f"{d[1]} ({d[2]})"})
        return ex

    def get_exhibits_rented_out(order_id) -> list:
        data = select_where("order_hold_exhibits", "order_id", order_id)
        ex = []

        for i in data:
            ex_id = int(i[1])
            d = select_one_where("exhibits", ["exhibit_id", "status"], [ex_id, 2])
            if d: ex.append({"id": int(d[0]), "name": d[1], "owner": d[2], "status": int(d[3]),
                                 "input": f"{d[1]} ({d[2]})"})
        return ex

    def get_orders():
        data: sqlite3.Row = select_all("order_hold")
        orders = []
        for d in data:
            orders.append({"date": d[1], "exhibition_id": int(d[2]), "id": int(d[0]),
                           "place": d[3], "input": f"{d[0]}. {d[1]} ({d[3]})", "status": int(d[4])
                          })
        return orders  

    def get_order(order_id):
        d = select_one_where("order_hold", ["order_id"], [order_id])
        order = {}
        if d:  order = ({"date": d[1], "exhibition_id": int(d[2]), "id": int(d[0]), "status": int(d[4]),
                         "place": d[3], "input": f"{d[0]}. {d[1]} ({d[3]})"})
        return order

    def delete_order(order_id):
        delete_where("order_hold", "order_id", order_id)




class Order_get:
    def __init__(self, date, order_id: int, exhibits: list[dict]):
        self.id = 0
        self.date = date
        self.order_id = order_id
        self.exhibits = exhibits

        self.insert_order_to_get()

    def insert_order_to_get(self):
        query = '''INSERT INTO order_get (id, date_get, order_id) 
                   VALUES(?, ?, ?);'''
        
        self.id = get_last_id("order_get", "id")+1
        execute_query(query, (self.id, self.date , self.order_id))
        
        Order_hold.change_status(1, self.order_id)
        for ex in self.exhibits:
            Exhibit.change_status(ex["id"], 1)
            print(f"[+] changed status of {ex['name']} to 1" )

        print("[+] order get added:", self.id)

    def get_hold_orders():
        data = select_all("order_get")
        orders = []
        for d in data:
            order_id = int(d[2])
            order = Order_hold.get_order(order_id)
            if order:
                orders.append(order)
        return orders



class Order_give:
    def __init__(self, date, order_id: int, exhibits: list[dict]):
        self.id = 0
        self.date = date
        self.order_id = order_id
        self.exhibits = exhibits

        self.insert_order_to_give()

    def insert_order_to_give(self):
        query = '''INSERT INTO order_give(id, date_give, order_id) 
                   VALUES(?, ?, ?);'''
        
        self.id = get_last_id("order_give", "id")+1
        execute_query(query, (self.id, self.date , self.order_id))
        
        Order_hold.change_status(2, self.order_id)
        for ex in self.exhibits:
            Exhibit.change_status(ex["id"], 2)
            print(f"[+] changed status of {ex['name']} to 2" )

        print("[+] order give added:", self.id)
    
    def get_get_orders():
        data = select_all("order_give")

        orders = []
        for d in data:
            order_id = int(d[2])
            order = Order_hold.get_order(order_id)
            if order:
                orders.append(order)
        return orders


class Order_return:
    def __init__(self, date, order_id: int, exhibits: list[dict]):
        self.date = date
        self.order_id = order_id
        self.exhibits = exhibits
        
        self.insert_order_to_return()

    def insert_order_to_return(self):
        query = '''INSERT INTO order_return (id, date_return, order_id) 
                   VALUES(?, ?, ?);'''
        
        self.id = get_last_id("order_return", "id")+1
        execute_query(query, (self.id, self.date , self.order_id))
        Order_hold.change_status(3, self.order_id)
        for ex in self.exhibits:
            Exhibit.change_status(ex["id"], 0)
            print(f"[+] changed status of {ex['name']} to 0" )

        print("[+] order return added:", self.id)
