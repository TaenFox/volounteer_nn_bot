from hashlib import new
from re import L
import sys 
import os.path
from urllib.parse import uses_netloc
from model import my_resource
from model import history

from model.myclass import MyClass 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db

class StorageUser(MyClass):
    description = ''
    def __init__(self, tgid, name):
        id = is_user_exist(tgid)
        super().__init__(id, 'storages')
        if id==0:
            self.prop.update({"tgid":tgid})
        self.prop.update({"name":name})
        self.update_data()

    def description_update(self):
# получить сообщение с текущим статусом пользователя
        if self.prop.get('banned')==True:
            ban = 'да'
        else:
            ban = 'нет'
        if self.prop.get('moderator')==True:
            moder = 'да'
        else:
            moder = 'нет'
        if self.prop.get('admin')==True:
            admin = 'да'
        else:
            admin = 'нет'
        self.description = f'Пользователь @{self.prop.get("name")}:\n\
Забанен: {ban}\n\
Модератор: {moder}\n\
Администратор: {admin}'
        return self.description


    def do_admin(self, auth_id):
        i = 1
        if self.prop.get("admin")==0:
            i=1
        else:
            i=0
        self.prop.update({"admin":i})
        history.do_history_storage('admin', i, auth_id)
        self.prop.update({"moderator":i})
        history.do_history_storage('moderator', i, auth_id)
        self.update_data()
        return i
    
    def do_moderator(self, auth_id):
        i = 1
        if self.prop.get("moderator")==0:
            i=1
        else:
            i=0
        self.prop.update({"moderator":i})
        history.History('storages', 'moderator', i, auth_id)
        self.update_data()
        return i

    def do_ban(self, auth_id):
        i = 1
        if self.prop.get("banned")==0:
            i=1
        else:
            i=0
        self.prop.update({"banned":i})
        history.History('storages', 'banned', i, auth_id)
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

def get_tgid(id):
    try:
        db.cursor.execute(f"SELECT `tgid` FROM {db.db_base}.storages WHERE `id`='{id}'")
        return db.cursor.fetchone()[0]
    except:
        return 0

def get_tgname(id):
    try:
        db.cursor.execute(f"SELECT `name` FROM {db.db_base}.storages WHERE `id`='{id}'")
        return db.cursor.fetchone()[0]
    except:
        return 0