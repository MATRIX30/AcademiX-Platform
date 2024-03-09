#!/usr/bin/pythonn3
"""module to handle course"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import event


storage_type = models.storage_type

class Course(BaseModel, Base):
    """class to manage courses"""
    
    if storage_type == 'db':
        __tablename__ = "courses"
        code = Column(String(7), nullable=False, primary_key=True)
        title = Column(String(60), nullable=False)
        coeff = Column(Integer, nullable=False, default=2)
        teacher_id = Column(String(60), ForeignKey('teachers.id'),nullable=False)
        class_id = Column(String(60), ForeignKey('classes.code'), nullable=False)
        
        # relationships
        # students = relationship("Student", backref='course')

      
    else:
        code = ""
        title = ""
        coeff = 2
        teacher_id = ""
        class_id = ""
        
    def __init__(self, *args, **kwargs):
        """initializes a course"""
        from models.teacher import Teacher
        super().__init__(*args, **kwargs)
        
