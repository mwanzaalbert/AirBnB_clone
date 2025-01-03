#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
User module for managing User objects.

This module defines the User class, which inherits from BaseModel and provides
additional attributes specific to a user. It also integrates with the storage
engine for persistence.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"


from models.base_model import BaseModel


class User(BaseModel):
    """Defines a User model extending BaseModel."""

    # Initialize attributes with default values
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize a new User instance.

        Args_:
            *args: Unused.
            **kwargs: Key-value pairs for initializing attributes.

        If `kwargs` is provided, attributes are set using the key-value pairs.
        Otherwise, default attribute values are initialized.
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    from models import storage
    # Example usage of the User class

    print("-- Create a new object --")
    my_user = User()
    my_user.first_name = "Betty"
    my_user.last_name = "Bar"
    my_user.email = "airbnb@mail.com"
    my_user.password = "root"
    print(my_user)

    # Save the object and display its updated state
    my_user.save()
    print(my_user)

    # Convert the object to a dictionary and display it
    print(my_user.to_dict())

    # Retrieve and display all objects from storage
    all_objs = storage.all()
    print("-- Reloaded objects --")
    for obj_id in all_objs.keys():
        obj = all_objs[obj_id]
        print(obj)
