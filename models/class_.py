#!/usr/bin/pythonn3
"""module to handle class"""

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models import storage_type

class Class(BaseModel, Base):
    """class to manage Class"""
    if storage_type == "db":
        __tablename__ = "classes"
        name = Column(String(60), nullable=False)
        code = Column(String(10), nullable=False, primary_key=True)
        number_of_students = Column(Integer, nullable=False)
        # relationship between class and courses offered
        courses = relationship("Course", backref="class_", cascade="all, delete, delete-orphan")
        students = relationship("Student", backref="class_", cascade="all, delete, delete-orphan")
    else:
        name = ""
        code = ""
        number_of_students = 0
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    if storage_type != "db":
        @property
        def courses(self):
            """getter for the courses offered in a class"""
            from models.course import Course
            course_list = []
            for course in models.storage.all(Course).values():
                if course.class_id  == self.id:
                    course_list.append(course)
            return course_list
        
        @property
        def students(self):
            """getter for the students in a class"""
            from models.student import Student
            student_list = []
            for student in models.storage.all(Student).values():
                if student.class_id  == self.id:
                    student_list.append(student)
            return student_list
