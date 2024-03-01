#!/usr/bin/python3
"""module to handle admins"""


from models.base_model import Base

import os
from models.personnel import Personnel
from sqlalchemy import Column, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

storage_type = os.environ.get('ACADEMIX_TYPE_STORAGE')


class Admin(Personnel, Base):
    """class to handle admins"""
    if storage_type == 'db':
        __tablename__ = "admins"
        id = Column(String(60), ForeignKey('personnels.id'), nullable=False, primary_key=True)
        admin_type = Column(String(10), nullable=False)
        status = Column(SmallInteger, nullable=False, default=0)
        # admin_id = Column(String(60), nullable=False, primary_key=True)
    else:
        status = 0
        admin_type = ""
        # admin_id = ""
        
    def __init__(self, *args, **kwargs):
        """initializing admin"""
        super().__init__(*args, **kwargs)
