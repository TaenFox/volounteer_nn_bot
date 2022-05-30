import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db
from model import myclass

class History(myclass.MyClass):
    def __init__(self, table, id_row:int, field, value, operator:int) -> None:
        super().__init__(0, 'history')
        self.prop.update({"table" : table})
        self.prop.update({"id_row" : id_row})
        self.prop.update({"field" : field})
        self.prop.update({"new_value" : value})
        self.prop.update({"storage" : operator})
        self.update_data()

def do_history(table, field, value, operator):
    query = f"INSERT INTO `{db.db_base}`.`history`  \
        (`table`,`field`,`new_value`,`storage`) \
VALUES ('{table}','{field}','{value}','{operator}')"
    db.cursor.execute(query)
    db.conn.commit()

def do_history_storage(field, value, operator):
    do_history('storages', field, value, operator)