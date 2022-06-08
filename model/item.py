from operator import truediv
import sys 
import os.path

import mysqlx

from model.myclass import MyClass 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db

class Item(MyClass):
    def __init__(self, id):
        self.prop = {}
        super().__init__(id, "resources")
        if self.prop.get('category')== None:
            self.category = ""
        else:
            self.category = Category(self.prop.get('category'))

    def set_category(self, id):
        self.prop.update({"category":id})
        self.update_data()

    def delete(self):
        self.prop.update({"is_deleted":1})
        self.update_data()


class Category(MyClass):
    def __init__(self, id):
        self.prop = {}
        super().__init__(id, 'categories')
        self.pub_name = self.prop.get('name')
        if self.prop.get('parent')!=None:
            self.parent = Category(self.prop.get('parent'))
            # self.pub_name = self.parent.pub_name + "->" + self.pub_name

    
def get_items(all = False):
    pass

def get_categories(name:str="", id:int=0):
    categories = []
    lookname = ""
    lookid = ""
    subquery = ""
    if name!="":
        lookname = f"`name` like '%{name}%' "
    if id!=0:
        lookid = f"`id` like '%{id}%' "
    if lookname!="":
        subquery = f"WHERE " + lookname
    if lookid != "":
        if subquery != "":
            subquery = subquery + lookid
        else:
            subquery = f"WHERE " + lookid            
    query = f'SELECT `id` FROM `{db.db_base}`.`categories` a {subquery} order by concat(if(isnull(a.`parent`),"",(select name from `{db.db_base}`.`categories` b where b.`id`=a.`parent`)), `name`)'
    for cat in db.select(query):
        categories.append(Category(cat[0]))
    return categories
