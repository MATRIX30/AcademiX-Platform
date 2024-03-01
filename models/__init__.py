#!/usr/bin/python3
"""file to make directory a package"""


from os import getenv

storage_type = getenv('ACADEMIX_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()