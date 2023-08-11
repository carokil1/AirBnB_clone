#!/usr/bin/python3
"""
    This is a package initializer
"""

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


storage = Filestorage()
storage.reload()
