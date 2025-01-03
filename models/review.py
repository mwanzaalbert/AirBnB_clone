#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Review module for managing Review objects.

This module defines the Review class, which is used to represent a review
for a place. The Review class inherits from the BaseModel class and includes
specific attributes for managing reviews, including place_id, user_id, and
text.

It also handles the initialization of a new review and storing it in the
database via the storage system.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

from datetime import datetime
from models.base_model import BaseModel


class Review(BaseModel):
    """A class that represents a review for a place.

    Inherits from the BaseModel class and adds specific attributes
    for managing reviews, including the place ID, user ID, and review text.
    The class also handles the initialization and storage of review instances.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Review instance.

        If keyword arguments are provided, it will initialize the instance
        attributes based on the provided values. Specifically, it will convert
        'created_at' and 'updated_at' fields from ISO format strings to
        datetime objects.

        If no keyword arguments are provided, it will initialize
        the place_id, user_id, and text attributes as empty strings.

        Args_:
            *args: Variable length argument list, passed to the parent class
                    initializer.

            **kwargs: Keyword arguments used to set the instance attributes,
                      expected to contain values for 'created_at',
                      'updated_at', 'place_id', 'user_id', and 'text'.

        Attributes_:
            place_id (str): The ID of the place being reviewed.
            user_id (str): The ID of the user submitting the review.
            text (str): The content of the review.
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)

        self.place_id: str = ""  # initialize to empty string
        # it will be the Place.id

        self.user_id: str = ""  # initialize to empty string
        # it will be the User.id

        self.text: str = ""  # initialize to empty string

        # If kwargs are provided, update attributes
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)


if __name__ == "__main__":
    # Example usage of the Review class
    user_review = Review()
    user_review.save()
    print(user_review)
