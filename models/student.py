#!/usr/bin/pythonn3
"""module to handle students"""

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, PrimaryKeyConstraint, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# creation of intermediate table to relate student to courses
if models.storage_type == "db":
    student_course= Table('student_course', Base.metadata,
                        Column('student_id', String(60),
                                ForeignKey('students.registration_number', onupdate='CASCADE', ondelete='CASCADE'),
                                primary_key=True),
                        Column('course_id', String(60), 
                                ForeignKey('courses.code', onupdate='CASCADE', ondelete='CASCADE'),
                                primary_key=True),
                        Column('first_seq', Float, default=0.0),
                        Column('second_seq', Float, default=0.0),
                        Column('third_seq', Float, default=0.0),
                        Column('fourth_seq', Float, default=0.0),
                        Column('fifth_seq', Float, default=0.0),
                        Column('sixth_seq', Float, default=0.0)          
    )

storage_type = models.storage_type
class Student(BaseModel, Base):
    """class to handle students"""
    if storage_type == "db":
        __tablename__ = "students"
        first_name = Column(String(60), nullable=False)
        last_name = Column(String(60), nullable=False)
        registration_number = Column(String(60), nullable=False, primary_key=True)
        class_id = Column(String(60), ForeignKey("classes.code"), nullable=True)
        email = Column(String(60), nullable=True)
        password = Column(String(60), nullable=True)
        # relationships
        courses = relationship("Course", secondary=student_course,
                               backref='student_courses',viewonly=False, passive_updates=True)
        
    else:
        first_name = ""
        last_name = ""
        registration_id = ""
        class_id = ""
        course_ids = []
        
    def __init__(self, *args, **kwargs):
        """initializer for student class"""
        super().__init__(*args, **kwargs)
        
    if storage_type != "db":
        @property
        def courses(self):
            """getter for courses"""
            from models.course import Course
            course_list = []
            all_courses = models.storage.all(Course)
            for course in all_courses:
                if course.class_id == self.class_id:
                    course_list.append(course)
            return course_list