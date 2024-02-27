#!/usr/bin/python3
"""Filestorage module"""
import json
import os
from models.base_model import BaseModel
from json.decoder import JSONDecodeError


class FileStorage:
    """class to manage file storage"""
    __file_path = "file.json"
    __objects = {}
    
    def all(self):
        """returns all objects in storage"""
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
