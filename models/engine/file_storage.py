#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
FileStorage module for object serialization and deserialization.

This module provides the FileStorage class for saving objects to a file in
JSON format and reloading them when needed. It supports basic CRUD operations
and lazy loading of classes.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
import json


class FileStorage:
    """
    Handles serialization and deserialization of objects to/from a JSON file.
    """
    __file_path = "file.json"
    __objects: dict = {}

    def all(self):
        """Retrieve all objects from storage.

        Returns_:
            dict: A dictionary of all objects in storage, re-instantiated to
            their original types.
        """
        self.reload()  # Ensure the latest objects are loaded

        return_dict = {}

        # Lazy imports to avoid circular dependencies
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        class_models = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

        # Convert stored dictionary representations back into objects
        for key, value in FileStorage.__objects.copy().items():
            cls, _ = key.split(".")
            return_dict[key] = class_models[cls](**value)

        return return_dict

    def new(self, obj):
        """Add a new object to the storage.

        Args_:
            obj (BaseModel or subclass): The object to add to storage.
        """
        FileStorage.__objects[f"{type(obj).__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """Serialize the __objects dictionary to the JSON file."""
        with open(FileStorage.__file_path, 'w') as outfile:
            json.dump(FileStorage.__objects, outfile)

    def reload(self):
        """
        Deserialize objects from the JSON file into the __objects dictionary,
        if the file exists.
        """
        try:
            if os.path.exists(FileStorage.__file_path):
                with open(FileStorage.__file_path, 'r') as infile:
                    FileStorage.__objects = json.load(infile)
        except Exception:
            pass
