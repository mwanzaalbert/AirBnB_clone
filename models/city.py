#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
City module for managing City objects.

This module defines the City class, which is used to represent a city
in the system. The City class inherits from the BaseModel class and
includes the name attribute, which stores the name of the city.
It also handles the initialization and storage of city instances.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

from datetime import datetime
from models.base_model import BaseModel


class City(BaseModel):
    """
    A class that represents a city.

    Inherits from the BaseModel class and adds a name attribute to store
    the name of the city. The class also handles the initialization and
    storage of city instances in the system.

    Attribute
        name (str): The name of the city.
    """

    # initialize to empty string
    name: str = ""
    state_id: str = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize a new City instance.

        If keyword arguments are provided, it will initialize the instance
        attributes based on the provided values. Specifically, it will convert
        'created_at' and 'updated_at' fields from ISO format strings to
        datetime objects.

        If no keyword arguments are provided, it will initialize
        the name attribute as an empty string.

        Args_:
            *args: Variable length argument list, passed to the parent class
            initializer.


            **kwargs: Keyword arguments used to set the instance attributes
            expected to contain values for 'created_at', 'updated_at', and
            'name'.

        Attributes_:
            name (str): The name of the city.
            state_id (str) : The id of the city's State
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    # Example usage of the City class
    my_city = City()
    my_city.name = "Los Angeles"
    my_city.save()
    print(my_city)

    my_newCity = City(**my_city.to_dict())
    print(my_newCity)
    print(type(my_newCity.updated_at))
