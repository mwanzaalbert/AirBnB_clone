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

from models.base_model import BaseModel


class Review(BaseModel):
    """
    A class that represents a review for a place.

    Inherits from the BaseModel class and adds specific attributes
    for managing reviews, including the place ID, user ID, and review text.
    The class also handles the initialization and storage of review instances.
    """

    # initialize to empty string
    place_id: str = ""

    user_id: str = ""

    text: str = ""

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


if __name__ == "__main__":
    # Example usage of the Review class
    user_review = Review()
    user_review.place_id = "Kempinksi"
    user_review.user_id = "usr0001"
    user_review.save()
    print(user_review)

    my_newReview = Review(**user_review.to_dict())
    print(my_newReview)
    print(type(my_newReview.updated_at))
