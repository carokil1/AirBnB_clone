#!/usr/bin/python3
"""
    Defines the class FileStorage
"""
import json
import models

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = str(obj.__class__.__name__) + '.' + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        """
        serializes __objects to the JSON file
        """
        o_dict = FileStorage.__objects
        obj_dict = {obj: o_dict[obj].to_dict() for obj in o_dict.keys()}
        with open(Filestorage.__file_path, encoding="UTF8", mode="w") as json_file:
            json.dump(obj_dict, json_file)

    def reload(self):
        """
        deserializes the JSON file to __objects
        """
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as json_file:
                FileStorage.__objects = json.load(json_file)
            for key, value in FileStorage.__objects.items():
                class_name = value["__class__"]
                class_def = models.classes[class_name]
                FileStorage.__objects[key] = class_def(**value)
        except FileNotFoundError:
            pass
