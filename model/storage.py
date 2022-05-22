from re import L
import sys 
import copy
import os.path
from urllib.parse import uses_netloc
from model import my_resource

from model.myclass import MyClass 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db

class StorageUser(MyClass):
    def __init__(self, tgid, name):
        id = is_user_exist(tgid)
        super().__init__(id, 'storages')
        if id==0:
            self.prop.update({"tgid":tgid})
        self.prop.update({"name":name})
        self.update_data()

    def do_admin(self):
        i = 1
        if self.prop.get("admin")==0:
            i=1
        else:
            i=0
        self.prop.update({"admin":i})
        self.prop.update({"moderator":i})
        self.update_data()
        return i
    
    def do_moderator(self):
        i = 1
        if self.prop.get("moderator")==0:
            i=1
        else:
            i=0
        self.prop.update({"moderator":i})
        self.update_data()
        return i

    def do_ban(self):
        i = 1
        if self.prop.get("banned")==0:
            i=1
        else:
            i=0
        self.prop.update({"banned":i})
        self.update_data()
        return i

    def add_resource(self):
        r = my_resource.Resource(0)
        r.prop.update({'storage':self.id})
        r.update_data()
        return r


class StoragePlace(MyClass):
    def __init__(self, id):
        super().__init__(id, 'storages')
        self.prop.update({"person":0})
        self.update_data()

def get_users(name:str="", id:int=0):
    users = []
    lookname = ""
    lookid = ""
    if name!="":
        lookname = f" and `name` like '%{name}%'"
    if id!=0:
        lookid = f" and `id` like '%{id}%'"
    query = f'SELECT `id`, `name` FROM `{db.db_base}`.`storages` WHERE `person`=1{lookname}{lookid}'
    print(query)
    list_of_users = db.select(query)
    return list_of_users



def is_user_exist(tgid):
    try:
        db.cursor.execute(f"SELECT `id` FROM {db.db_base}.storages WHERE `tgid`='{tgid}'")
        return db.cursor.fetchone()[0]
    except:
        return 0