#!/usr/bin/pythonn3
"""module to handle teachers"""
import models
from models.base_model import Base
from models.personnel import Personnel


from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship



class Teacher(Personnel, Base):
    """class to manage teacher"""
    
    if models.storage_type == 'db':
        __tablename__ = "teachers"
        matricule = Column(String(8),nullable=False, primary_key=True)
        grade = Column(String(10), nullable=False, default="ECI")
        position = Column(String(25), nullable=False)
        id = Column(String(60), ForeignKey('personnels.id'), nullable=False)
        # relationship with Course table
        courses = relationship("Course", backref="teacher", cascade="all, delete, delete-orphan")
    else:
        matricule = ""
        grade = ""
        position = ""

    def __init__(self, *args, **kwargs):
        """instantiation of Teacher object"""
        super().__init__(*args, **kwargs)
    
    if models.storage_type != "db":
        @property
        def courses(self):
            """getter for list of courses taught by a teacher"""
            from models.course import Course
            course_list = []
            for course in models.storage.all(Course).values():
                if self.id == course.teacher_id:
                    course_list.append(course)
            return course_list
