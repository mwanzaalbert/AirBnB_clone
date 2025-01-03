#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""BaseModel module defines abstract class managing other models objects."""
import uuid
from datetime import datetime
from models import storage

__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"


class BaseModel:
    """
    Defines common attributes and methods for all models in the system.

    Attributes_:
        id (str): A unique identifier for the instance.
        created_at (datetime): Timestamp of when the instance was created.
        updated_at (datetime): Timestamp of the last update to the instance.

    Methods_:
        save: Updates the instance's updated_at attribute and saves it.
        to_dict: Returns a dictionary representation of the instance.
        __str__: Returns a string representation of the instance.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel instance.

        If keyword arguments are provided, it sets the attributes from
        the kwargs dictionary, converting the 'created_at' and 'updated_at'
        fields to datetime objects from ISO format strings. If no arguments
        are provided, it generates a unique ID and assigns the current
        datetime to the 'created_at' and 'updated_at' attributes.

        Args_:
            *args: Variable length argument list, passed to the parent class
            initializer.


            **kwargs: Keyword arguments used to set instance attributes.
        """
        self.id: str = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

        storage.new(self)

    def save(self):
        """
        Update the 'updated_at' attribute of the instance and saves it.

        The instance's updated_at field is updated to the current datetime
        before the instance is saved in the storage.

        This method also triggers a call to the `storage.save()` method to
        persist the updated instance in storage.

        Note_:
            The storage system stores the instance by the key
            "{class_name}.{id}".
        """
        self.updated_at = datetime.now()

        key = f"{type(self).__name__}.{self.id}"

        if key in storage._FileStorage__objects:
            storage._FileStorage__objects[key].update(self.to_dict())
        else:
            storage._FileStorage__objects[key] = self.to_dict()

        storage.save()

    def to_dict(self):
        """
        Convert the instance to a dictionary representation.

        This method returns a dictionary where the key-value pairs are the
        attributes of the instance. The 'created_at' and 'updated_at' fields
        are converted to ISO 8601 string format.

        Returns_:
            dict: A dictionary representation of the instance, including the
                  class name and the attributes (with 'created_at' and
                                                 'updated_at' in ISO format).
        """
        return_dict = {"__class__": type(self).__name__}

        for key, value in self.__dict__.copy().items():
            if key in ("created_at", "updated_at"):
                return_dict[key] = value.isoformat()
            else:
                return_dict[key] = value

        return return_dict

    def __str__(self):
        """
        Return a string representation of the instance.

        The string format is:
        [ClassName] (id) {'attribute1': value1, 'attribute2': value2, ...}

        Returns_:
            str: A string representation of the instance.
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My First Model"
    my_model.my_number = 89
    print(my_model)
    my_model.save()
    print(my_model)
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key,
              type(my_model_json[key]), my_model_json[key]))

    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print("my_new_model", type(my_new_model.created_at))
    print("my_new_model", type(my_new_model.my_number))

    print("--")
    print(my_model is my_new_model)

    all_objs = storage.all()
    print("-- Reloaded objects --")
    for obj_id in all_objs.keys():
        obj = all_objs[obj_id]
        print(obj)

    print("-- Create a new object --")
    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89

    my_model.save()
    print(my_model)

    print(storage._FileStorage__objects)
