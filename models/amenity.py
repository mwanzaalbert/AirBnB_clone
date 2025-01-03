#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Amenity module for managing Amenity objects.

This module defines the Amenity class, which is used to represent an amenity
in the system. The Amenity class inherits from the BaseModel class and
includes the name attribute, which stores the name of the amenity.
It also handles the initialization and storage of amenity instances.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

from datetime import datetime
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    A class that represents an amenity.

    Inherits from the BaseModel class and adds a name attribute to store
    the name of the amenity. The class also handles the initialization and
    storage of amenity instances in the system.

    Attributes_:
        name (str): The name of the amenity.
    """

    name: str = ""  # initialize to empty string

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Amenity instance.

        If keyword arguments are provided, it will initialize the instance
        attributes based on the provided values. Specifically, it will convert
        'created_at' and 'updated_at' fields from ISO format strings to
        datetime objects.

        If no keyword arguments are provided, it will initialize
        the name attribute as an empty string.

        Args_:
            *args: Variable length argument list, passed to the parent class
            initializer.


            **kwargs: Keyword arguments used to set the instance attributes,
                      expected to contain values for 'created_at',
                      'updated_at', and 'name'.

        Attributes_:
            name (str): The name of the amenity.
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    # Example usage of the Amenity class
    my_amenity = Amenity()
    my_amenity.name = "Penthouse"
    my_amenity.save()
    print(my_amenity)

    my_newAmenity = Amenity(**my_amenity.to_dict())
    print(my_newAmenity)
    print(type(my_newAmenity.updated_at))
