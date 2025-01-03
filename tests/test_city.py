#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the City class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import unittest
import os
import json
import time
from datetime import datetime
from models.city import City
from models import storage


class TestCity(unittest.TestCase):
    """
    Test suite for the City class.
    """

    def setUp(self):
        """Set up resources for the tests."""
        self.city = City()

        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up resources after tests."""

        # Remove the JSON file if it exists
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.city

        storage._FileStorage__objects.clear()

    def test_instance_creation(self):
        """Test if City instance is created properly."""
        self.assertIsInstance(self.city, City)

    def test_name_initialization(self):
        """Test that the name attribute is initialized as an empty string."""
        self.assertEqual(self.city.name, "")

    def test_name_assignment(self):
        """Test assignment of the name attribute."""
        self.city.name = "New York"
        self.assertEqual(self.city.name, "New York")

    def test_city_attributes(self):
        """Test City attributes."""
        obj = City()
        self.assertTrue(hasattr(obj, "name"))

    def test_kwargs_initialization(self):
        """Test initialization using kwargs."""
        created_time = datetime.now().isoformat()
        updated_time = datetime.now().isoformat()
        city = City(name="San Francisco", created_at=created_time,
                    updated_at=updated_time)
        self.assertEqual(city.name, "San Francisco")
        self.assertIsInstance(city.created_at, datetime)
        self.assertIsInstance(city.updated_at, datetime)
        self.assertEqual(city.created_at.isoformat(), created_time)
        self.assertEqual(city.updated_at.isoformat(), updated_time)

    def test_save_method_updates_updated_at(self):
        """Test the save method updates the updated_at attribute."""
        old_updated_at = self.city.updated_at
        time.sleep(5)
        self.city.save()
        self.assertNotEqual(self.city.updated_at, old_updated_at)
        self.assertTrue(hasattr(self.city, "updated_at"))

    def test_storage_new_called(self):
        """Test that the City instance is added to storage."""
        self.assertIn(f"{type(self.city).__name__}.{self.city.id}",
                      storage.all())

    def test_object_saved_to_json(self):
        """Test that the City object is saved to the JSON file."""
        self.city.name = "Paris"
        self.city.save()
        storage.save()  # Save all objects to the file
        with open("file.json", "r") as f:
            data = json.load(f)
            key = f"City.{self.city.id}"
            self.assertIn(key, data)
            self.assertEqual(data[key]["name"], "Paris")

    def test_object_retrieved_from_storage(self):
        """Test that the object can be reloaded from the JSON file."""
        self.city.name = "Berlin"
        self.city.save()
        storage.save()  # Save all objects to the file
        storage.reload()  # Reload objects from the file
        key = f"City.{self.city.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Berlin")


if __name__ == "__main__":
    unittest.main()
