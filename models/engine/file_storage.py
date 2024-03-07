#!/usr/bin/python3
"""Filestorage module"""
import json
import os
from models.base_model import BaseModel
from models.admin import Admin
from models.teacher import Teacher
from models.class_ import Class
from models.course import Course
from models.personnel import Personnel
from models.student import Student
from json.decoder import JSONDecodeError


class FileStorage:
    """class to manage file storage"""
    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        """returns all objects in storage"""
        
        if cls:
            available_classes = [class_.split('.')[0] for class_ in FileStorage.__objects.keys()]
            res = {}
            if cls in available_classes:
                for key, obj in FileStorage.__objects.items():
                    if cls == key.split('.')[0]:
                        res[key] = obj
                return res
        return FileStorage.__objects
    
    def new(self, obj):
        """creates a new object obj in storage"""
        obj_key = "{}.{}".format(obj.__class__.__name__,obj.id)
        FileStorage.__objects[obj_key] = obj
        
    def save(self):
        """saves __objects to __file_path"""
        data = {key: obj.to_dict() for key, obj in FileStorage.__objects.items() }
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(data, file)
    
    def reload(self):
        """method to reload objects from __file_path"""
        
        if os.path.exists(FileStorage.__file_path):
            try:
                with open(FileStorage.__file_path, 'r') as file:
                    json_objects = json.load(file)
            except JSONDecodeError:
                """do nothing if decode error occurs"""
                return
            res_objs = {}
            for obj_key, obj in json_objects.items():
                res_objs[obj_key] = eval(obj["__class__"])(**obj)
            FileStorage.__objects = res_objs
            
    def delete(self, obj=None):
        """method to delete object from objects"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects.keys():
                FileStorage.__objects.pop(key, None)
            self.save()
                
    def close(self):
        """calls reload method for deserializing the json file to objects"""
        self.reload()
    
    def count(self, cls=None):
        """method to return the number of objects in fs"""
        count = 0
        result = {}
        if cls is None:
            return len(self.__objects)
        
    def get(self, cls, id):
        """method to get an object by id"""
        for obj in self.__objects.keys():
            val = obj.split('.')[1]
            if val == id:
                return  self.__objects[obj]
