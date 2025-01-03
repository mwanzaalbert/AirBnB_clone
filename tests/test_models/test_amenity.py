#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the Amenity class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
import unittest
import time
from datetime import datetime
from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.amenity = Amenity()
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.amenity

        storage._FileStorage__objects.clear()

    def test_inheritance(self):
        """Test that Amenity inherits from BaseModel."""
        self.assertIsInstance(self.amenity, BaseModel)

    def test_default_attributes(self):
        """Test that default attributes are initialized correctly."""
        self.assertEqual(self.amenity.name, "")

    def test_amenity_attributes(self):
        """Test Amenity attributes."""
        obj = Amenity()
        self.assertTrue(hasattr(obj, "name"))

    def test_attribute_assignment(self):
        """Test that attributes can be assigned correctly."""
        self.amenity.name = "Pool"
        self.assertEqual(self.amenity.name, "Pool")

    def test_kwargs_initialization(self):
        """Test initialization using keyword arguments."""
        kwargs = {
            "id": "1234",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-02T12:00:00",
            "name": "Spa"
        }
        amenity = Amenity(**kwargs)
        self.assertEqual(amenity.id, "1234")
        self.assertEqual(amenity.created_at, datetime(2025, 1, 1, 12, 0, 0))
        self.assertEqual(amenity.updated_at, datetime(2025, 1, 2, 12, 0, 0))
        self.assertEqual(amenity.name, "Spa")

    def test_storage_interaction(self):
        """Test that the Amenity instance interacts with storage."""
        self.assertIn(f"{type(self.amenity).__name__}.{self.amenity.id}",
                      storage.all())

        new_amenity = Amenity()
        self.assertIn(f"{type(new_amenity).__name__}.{new_amenity.id}",
                      storage.all())

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.amenity.updated_at
        time.sleep(5)
        self.amenity.save()
        self.assertNotEqual(self.amenity.updated_at, old_updated_at)

    def test_to_dict_contains_name(self):
        """Test that to_dict() includes the name attribute."""
        self.amenity.name = "Garden"
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["name"], "Garden")

    def test_str_representation(self):
        """Test the string representation of the Amenity instance."""
        expected_str = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), expected_str)


if __name__ == "__main__":
    unittest.main()
