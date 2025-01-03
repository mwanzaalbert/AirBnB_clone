#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
State module for managing State objects.

This module defines the State class, which is used to represent a state
in the system. The State class inherits from the BaseModel class and
includes the name attribute, which stores the name of the state.
It also handles the initialization and storage of state instances.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

from models.base_model import BaseModel


class State(BaseModel):
    """
    A class that represents a state.

    Inherits from the BaseModel class and adds a name attribute to store
    the name of the state. The class also handles the initialization and
    storage of state instances in the system.

    Attributes_:
        name (str): The name of the state.
    """

    name: str = ""  # initialize to empty string

    def __init__(self, *args, **kwargs):
        """
        Initialize a new State instance.

        If keyword arguments are provided, it will initialize the instance
        attributes based on the provided values. Specifically, it will convert
        'created_at' and 'updated_at' fields from ISO format strings to
        datetime objects. If no keyword arguments are provided, it will
        initialize the name attribute as an empty string.

        Args_:
            *args: Variable length argument list, passed to the parent class
            initializer.

            **kwargs: Keyword arguments used to set the instance attributes,
            expected to contain values for 'created_at', 'updated_at', and
            'name'.

        Attributes_:
            name (str): The name of the state.
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    # Example usage of the State class
    my_state = State()
    my_state.name = "California"
    my_state.save()
    print(my_state)
    print()
    print(my_state.to_dict())

    my_newState = State(**my_state.to_dict())
    print(my_newState)
    print(type(my_newState.updated_at))
