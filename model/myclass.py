from operator import truediv
import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db

class MyClass:
    
    prop = {}
    id = 0
    table = ""
    isnew = False

    def __init__(self, id, table) -> None:
        self.id=id
        self.table=table

        if id==0:
            db.cursor.execute(f"INSERT INTO {db.db_base}.{table} values ()")
            self.id= db.cursor.lastrowid
            db.conn.commit()
            id = self.id
        db.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='{table}'")
        fields = db.cursor.fetchall()
        columns = []
        for field in fields:
            columns.append('`'+field[0]+'`')
        column_query = ", ".join(columns)
        db.cursor.execute(f"SELECT {column_query} FROM {db.db_base}.{table} WHERE ID = {id}")
        data = db.cursor.fetchone()

        i = -1
        for field in fields:
            i += 1
            self.prop.update({field[0]:data[i]})

    def update_data(self):
                
        query = ','.join([f'`{key}`="{value}"' for key, value in self.prop.items()]) 
        query = f"UPDATE `{db.db_base}`.`{self.table}` SET {query} WHERE `id` = {self.id}"
        db.cursor.execute(query)
        db.conn.commit()
        
# a = MyClass(8,'apples')
# a.prop.update({"apple":"123"})
# a.update_data()