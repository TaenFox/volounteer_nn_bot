import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db
from model import myclass

class History(myclass.MyClass):
    def __init__(self, table, id_row:int, field, value, operator:int) -> None:
        self.prop = {}
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

class Payload(myclass.MyClass):
    def __init__(self, inline_message_id, query='', result_id=0) -> None:
        
        id = self.is_exist_inline_message_id(inline_message_id)

        self.prop = {
            'inline_message_id' : inline_message_id,
            'query' : query,
            'result_id' : result_id
        }
        self.id=id

        if id==0:
            query = f"INSERT INTO `{db.db_base}`.`payload` \
                                (`inline_message_id`, `query`, `result_id`) \
                        values (\'{inline_message_id}\',\'{query}\',\'{result_id}\')"
            db.cursor.execute(query)
            self.id= db.cursor.lastrowid
            db.conn.commit()
            id = self.id
            self.isnew = True
        super().__init__(id, 'payload')


    def is_exist_inline_message_id(self, inline_message_id):
        query = f'SELECT `id` FROM `{db.db_base}`.`payload` WHERE `inline_message_id` = \'{inline_message_id}\' LIMIT 1'
        db.cursor.execute(query)
        
        try:
            db.conn.commit()
            query_result = db.cursor.fetchone()[0]
            if query_result != None:
                result = query_result
            else:
                result = 0
        except:
            result=0
        return result

    def terminate_old():
        too_old = 10        # поменяй значение чтобы увеличить срок жизни кэша кнопок
        select_query = f'SELECT `id` FROM `{db.db_base}`.`payload` WHERE `dateadd` < NOW() - INTERVAL {too_old} MINUTE'
        db.cursor.execute(select_query)
        db.conn.commit()
        for i in db.cursor.fetchall():
            delete_query = f'DELETE FROM `{db.db_base}`.`payload` WHERE `id` = {i[0]} '
            db.cursor.execute(delete_query)
            db.conn.commit()

    def terminate(self):
        delete_query = f'DELETE FROM `{db.db_base}`.`payload` WHERE `id` = {self.id} '
        db.cursor.execute(delete_query)
        db.conn.commit()