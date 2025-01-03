#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Place module for managing Place objects.

This module defines the Place class, which is used to represent a place
in the system. The Place class inherits from the BaseModel class and includes
various attributes related to a place, such as the city, user, name
description,rooms, price, and amenities. It also handles the initialization
and storage of place instances.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

from typing import List
from models.base_model import BaseModel


class Place(BaseModel):
    """
    A class that represents a place.

    Inherits from the BaseModel class and adds several attributes such as
    the city and user IDs, name, description, number of rooms and bathrooms,
    maximum number of guests, price per night, latitude, longitude, and a list
    of amenity IDs. The class also handles the initialization and storage of
    place instances in the system.

    Attributes_:
        city_id (str): The ID of the city where the place is located.
        user_id (str): The ID of the user who created the place.
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum No. of guests the place can accommodate.
        price_by_night (int): The price per night to rent the place.
        latitude (float): The latitude of the place's location.
        longitude (float): The longitude of the place's location.
        amenity_ids (List[str]): A list of amenity IDs associated with a
                                place.
    """

    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: List[str] = []

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Place instance.

        If keyword arguments are provided, it will initialize the instance
        attributes based on the provided values. Specifically, it will convert
        'created_at' and 'updated_at' fields from ISO format strings to
        datetime objects.

        If no keyword arguments are provided, it will initialize the
        attributes such as `city_id`, `user_id`, `name`, `description`, and
        other fields with default values.

        Args_:
            *args: Variable length argument list, passed to the parent class
                    initializer.

            **kwargs: Keyword arguments used to set the instance attributes,
                      expected to contain values for 'created_at',
                      'updated_at', and other attributes.

        Attributes_:
            city_id (str): The ID of the city where the place is located.
            user_id (str): The ID of the user who created the place.
            name (str): The name of the place.
            description (str): A description of the place.
            number_rooms (int): The number of rooms in the place.
            number_bathrooms (int): The number of bathrooms in the place.
            max_guest (int): The maximum number of guests the place can
                             accommodate.
            price_by_night (int): The price per night to rent the place.
            latitude (float): The latitude of the place's location.
            longitude (float): The longitude of the place's location.
            amenity_ids (List[str]): A list of amenity IDs associated with the
                                    place.
        """
        # Call the BaseModel initializer
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    # Example usage of the Place class
    my_place = Place()
    my_place.name = "California"
    my_place.save()
    print(my_place)

    my_newPlace = Place(**my_place.to_dict())
    print(my_newPlace)
    print(type(my_newPlace.updated_at))
