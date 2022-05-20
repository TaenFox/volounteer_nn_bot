from operator import truediv
import sys 
import os.path

from model.myclass import MyClass 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
import db

class Resource(MyClass):
    def __init__(self, id):
        super().__init__(id, "resources")

    def delete(self):
        self.prop.update({"is_deleted":1})
        self.update_data()
