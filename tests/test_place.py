#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the Place class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from models.place import Place
from models import storage


class TestPlace(unittest.TestCase):
    def setUp(self):
        """Sets up a fresh Place instance before each test."""
        self.place = Place()
        self.kwargs = {
            "city_id": "123",
            "user_id": "456",
            "name": "California Villa",
            "description": "A beautiful villa in California",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 250,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "amenity_ids": ["wifi", "pool", "gym"],
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00"
        }

        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.place

        storage._FileStorage__objects.clear()

    def test_initialization_with_no_kwargs(self):
        """Test initializing Place with no kwargs."""
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])

    @patch("models.storage.new")
    def test_initialization_with_kwargs(self, mock_storage):
        """Test initializing Place with kwargs."""
        place = Place(**self.kwargs)
        self.assertEqual(place.city_id, "123")
        self.assertEqual(place.user_id, "456")
        self.assertEqual(place.name, "California Villa")
        self.assertEqual(place.description, "A beautiful villa in California")
        self.assertEqual(place.number_rooms, 3)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 6)
        self.assertEqual(place.price_by_night, 250)
        self.assertEqual(place.latitude, 34.0522)
        self.assertEqual(place.longitude, -118.2437)
        self.assertEqual(place.amenity_ids, ["wifi", "pool", "gym"])
        self.assertEqual(place.created_at,
                         datetime.fromisoformat("2025-01-01T12:00:00"))
        self.assertEqual(place.updated_at,
                         datetime.fromisoformat("2025-01-01T12:00:00"))
        mock_storage.assert_called_once_with(place)

    def test_init_with_invalid_kwargs(self):
        """Test initialization with invalid kwargs."""
        invalid_kwargs = {"invalid_key": "invalid_value"}
        place = Place(**invalid_kwargs)
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])

    def test_place_attributes(self):
        """Test Place attributes."""
        obj = Place()
        self.assertTrue(hasattr(obj, "city_id"))
        self.assertTrue(hasattr(obj, "user_id"))
        self.assertTrue(hasattr(obj, "name"))
        self.assertTrue(hasattr(obj, "description"))
        self.assertTrue(hasattr(obj, "number_rooms"))

    @patch("models.storage.save")
    def test_save(self, mock_save):
        """Test the save method."""
        self.place.save()
        mock_save.assert_called_once()

    def test_to_dict(self):
        """Test the to_dict method."""
        place = Place(**self.kwargs)
        place_dict = place.to_dict()
        self.assertEqual(place_dict["city_id"], "123")
        self.assertEqual(place_dict["user_id"], "456")
        self.assertEqual(place_dict["name"], "California Villa")
        self.assertEqual(place_dict["description"],
                         "A beautiful villa in California")
        self.assertEqual(place_dict["number_rooms"], 3)
        self.assertEqual(place_dict["number_bathrooms"], 2)
        self.assertEqual(place_dict["max_guest"], 6)
        self.assertEqual(place_dict["price_by_night"], 250)
        self.assertEqual(place_dict["latitude"], 34.0522)
        self.assertEqual(place_dict["longitude"], -118.2437)
        self.assertEqual(place_dict["amenity_ids"], ["wifi", "pool", "gym"])
        self.assertEqual(place_dict["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(place_dict["updated_at"], "2025-01-01T12:00:00")

    @patch("models.storage.new")
    def test_update_attributes(self, mock_storage):
        """Test updating attributes."""
        new_data = {
            "city_id": "789",
            "user_id": "101112",
            "name": "New York Penthouse",
            "description": "A luxury penthouse in NYC",
            "number_rooms": 5,
            "number_bathrooms": 4,
            "max_guest": 10,
            "price_by_night": 1000,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenity_ids": ["wifi", "jacuzzi", "spa"]
        }
        self.place.__dict__.update(new_data)
        self.assertEqual(self.place.city_id, "789")
        self.assertEqual(self.place.user_id, "101112")
        self.assertEqual(self.place.name, "New York Penthouse")
        self.assertEqual(self.place.description, "A luxury penthouse in NYC")
        self.assertEqual(self.place.number_rooms, 5)
        self.assertEqual(self.place.number_bathrooms, 4)
        self.assertEqual(self.place.max_guest, 10)
        self.assertEqual(self.place.price_by_night, 1000)
        self.assertEqual(self.place.latitude, 40.7128)
        self.assertEqual(self.place.longitude, -74.0060)
        self.assertEqual(self.place.amenity_ids, ["wifi", "jacuzzi", "spa"])

    @patch("models.storage.new")
    def test_saved_object(self, mock_storage):
        """Test that the Place object is properly saved using storage.new."""
        # Create a new Place instance
        place = Place(name="New Place", city_id="123", user_id="456")

        # Call save() method, which should trigger the storage.new method
        place.save()

        # Check if storage.new was called once with the place object
        mock_storage.assert_called_once_with(place)

        # Optionally, you can verify if other attributes are saved
        # Retrieve the saved place object
        saved_place = mock_storage.call_args[0][0]
        self.assertEqual(saved_place.name, "New Place")
        self.assertEqual(saved_place.city_id, "123")
        self.assertEqual(saved_place.user_id, "456")
        self.assertIsInstance(saved_place, Place)


if __name__ == "__main__":
    unittest.main()
