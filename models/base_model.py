#!/usr/bin/python3
"""Base model from which other models will inherite from"""

from datetime import datetime
from uuid import uuid4
import models

class BaseModel:
    """Base model class"""
    id:str
    created_at:datetime
    updated_at:datetime
    
    def __init__(self, *args, **kwargs):
        """
        constructor for Base Model class
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
    
    
    def __str__(self) -> str:
        """method to print the string representatio of object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """method to save new object to storage 
           and update instance updated time
        """
        self.updated_at = datetime.now()
        models.storage.save()
        
    def to_dict(self):
        """
        method to return dictionary representation of object
        """
        dict_repr = self.__dict__.copy()
        dict_repr["__class__"] = self.__class__.__name__
        dict_repr["created_at"] = dict_repr["created_at"].isoformat()
        dict_repr["updated_at"] = dict_repr["updated_at"].isoformat()
        return dict_repr