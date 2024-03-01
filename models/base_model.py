#!/usr/bin/python3
"""Base model from which other models will inherite from"""

from datetime import datetime
from uuid import uuid4
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """Base model class"""
    if models.storage_type == 'db':
        id = Column(String(60), unique=True, nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    

    def __init__(self, *args, **kwargs):
        """
        constructor for Base Model class
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    # verify if id is available and its string if not pass we will auto generate one
                    if key == 'id' and type(key) != str:
                        pass
                    setattr(self, key, value)
            if getattr(self, 'created_at', None) is None:
                setattr(self, 'created_at', datetime.now())
            if getattr(self, 'updated_at', None) is None:
                setattr(self, 'updated_at', datetime.now())
            if getattr(self, 'id', None) is None:
                setattr(self, 'id', str(uuid4()))
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            
    
    
    def __str__(self) -> str:
        """method to print the string representatio of object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """method to save new object to storage 
           and update instance updated time
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()
        
        
    def to_dict(self):
        """
        method to return dictionary representation of object
        """
        dict_repr = self.__dict__.copy()
        dict_repr["__class__"] = self.__class__.__name__
        dict_repr["created_at"] = dict_repr["created_at"].isoformat()
        dict_repr["updated_at"] = dict_repr["updated_at"].isoformat()
        dict_repr.pop("_sa_instance_state", None)
        return dict_repr
    def delete(self):
        """method to manage deletion of object"""
        models.storage.delete(self)
