#!/usr/bin/python3
"""module to manage db storage"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.personnel import Personnel
from models.admin import Admin
from models.class_ import Class
from models.teacher import Teacher
from models.course import Course
from models.student import Student
from sqlalchemy import event

classes = {"Teacher": Teacher, "Course":Course,
           "Class":Class, "Personnel": Personnel, "Admin":Admin,
           "BaseModel":BaseModel, "Student":Student}

class DBStorage:
    """class to manage database storage"""
    __engine=None
    __session=None
    
    def __init__(self):
        """instantiate a dbstorage object ie create a connection to db"""
        ACADEMIX_MYSQL_USER = getenv('ACADEMIX_MYSQL_USER')
        ACADEMIX_MYSQL_PWD = getenv('ACADEMIX_MYSQL_PWD')
        ACADEMIX_MYSQL_HOST = getenv('ACADEMIX_MYSQL_HOST')
        ACADEMIX_MYSQL_DB = getenv('ACADEMIX_MYSQL_DB')
        ACADEMIX_ENV = getenv('ACADEMIX_ENV')
        
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(ACADEMIX_MYSQL_USER,
                                             ACADEMIX_MYSQL_PWD,
                                             ACADEMIX_MYSQL_HOST,
                                             ACADEMIX_MYSQL_DB), pool_pre_ping=True)
        if ACADEMIX_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls=None):
        """method to get all objects of class name cls"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name___ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    
    """     @event.listens_for(Course, 'after_insert')
        def insert_student_courses(self, mapper, connection, target):
            # Get all students belonging to the class of the newly inserted course
            students = target.class_.students
            # Create entries in the student_course table for each student
            for student in students:
                self.__session.execute(student_course.insert().values(
                    student_id=student.registration_number,
                    course_id=target.code,
                    first_seq=0.0,
                    second_seq=0.0,
                    third_seq=0.0,
                    fourth_seq=0.0,
                    fifth_seq=0.0,
                    sixth_seq=0.0
                ))
        """
    def count(self, cls=None):
        """method to return the number of objects in db"""
        if cls is None:
            count = 0
            for cls in classes.values():
                count+=self.__session.query(cls).count()
            return (count)
        if cls not in classes.values() or cls not in classes.keys():
            return (0)
        return self.__session.query(cls).count()
    def get(self, cls, id):
        """method to get an object by id"""
        if cls not in classes.values() or cls not in classes.keys():
            return None
        return self.__session.query(cls).filter(id == cls.id).one_or_none()
    
    def new(self, obj):
        """method to add new class ne w== obj into  main storage engine"""
        self.__session.add(obj)
        
    def save(self):
        """save object to database"""
        self.__session.commit()
        
    def delete(self, obj=None):
        """Method to delete """
        if obj is not None:
            self.__session.delete(obj)
    
    def reload(self):
        """method to relaod database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session
    
    def close(self):
        """call remove() method on private session and close database"""
        self.__session.remove()
        
    def get_session(self):
        """get the current session"""
        return self.__session