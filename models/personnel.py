#!/usr/bin/python3
"""module to handle personnels"""


import models
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


storage_type = os.getenv('ACADEMIX_TYPE_STORAGE')
class Personnel(BaseModel, Base):
    """class to manage personnels"""
    
    if storage_type == 'db':
        __tablename__ = "personnels"
        first_name = Column(String(60), nullable=False)
        last_name = Column(String(60), nullable=False)
        email = Column(String(60), nullable=False)
        password = Column(String(128), nullable=False)
        
        # personnel can be admin or teacher
        admin = relationship("Admin", backref="personnel")
        teacher = relationship("Teacher", backref="personnel", cascade="all, delete, delete-orphan")
        
    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        
    def __init__(self, *args, **kwargs):
        """constructor of pesonnel"""
        super().__init__(*args, **kwargs)
        
    if storage_type != 'db':
        @property
        def teacher(self):
            """getter for teacher associated to personnel"""
            from models.teacher import Teacher
            all_teachers = models.storage.all(Teacher)
            # all_admins = models.storage.all(Admin)
            # person_is_a = None
            teacher = None
            
            for key in all_teachers.keys():
                if self.id == key.split('.')[1]:
                    teacher = all_teachers[key]
            return teacher
          
        @property
        def admin(self):
            """ getter for admin associated to personnel """
            from models.admin import Admin
            all_admins = models.storage.all(Admin)
            admin = None
            
            for key in all_admins.keys():
                if self.id == key.split('.')[1]:
                    admin = all_admins[key]
            return admin 
