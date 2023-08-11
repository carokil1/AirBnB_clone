#!/usr/bin/python3

"""This is a class BaseModel that defines all
common attributes/methods for other classes"""

import models #importing classes from the models module
import uuid
from datetime import datetime

class BaseModel:
    """This class represents the BaseModel of the AirBnB project."""

    def __init__(self, *args, **kwargs):
        """This initializes a new instance of BaseModel.

        Parameters:
            *args: Unused positional arguments.
            **kwargs: key/value pairs representing attributes.
        """

            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            if len(kwargs) != 0:
                for key, value, in kwargs.items():
                    if key == 'created_at' or key == 'updated_at':
                        self.__dict__[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    else:
                        self.__dict__[key] = value
            else:
                models.storage.new(self)

    def __str__(self):
        """
        This method returns a formatted string containing the class name,
        the instance's ID, and its attribute dictionary.

        Returns:
        str: A string representation of the object.
        """

        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Update 'updated_at' with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        This method creates a dictionary representation of the object's
        attributes e.g class name, creation timestamp, & the current timestamp.

        Returns: dict: A dictionary containing object attributes.
        """

        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
