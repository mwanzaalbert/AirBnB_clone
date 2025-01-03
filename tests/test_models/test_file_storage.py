#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the FileStorage class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.storage = FileStorage()
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        self.storage._FileStorage__objects.clear()

    def test_new(self):
        """Test adding a new object to storage."""
        obj = BaseModel()
        self.storage.new(obj)
        key = f"BaseModel.{obj.id}"

        self.assertIn(key, FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key]["id"], obj.id)

    def test_save_creates_file(self):
        """Test that save creates the JSON file."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        self.assertTrue(os.path.exists(self.file_path))

    def test_save_stores_correct_data(self):
        """Test that save correctly serializes objects to the file."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        with open(self.file_path, "r") as file:
            data = json.load(file)

        key = f"BaseModel.{obj.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["id"], obj.id)

    def test_reload_loads_data(self):
        """Test that reload correctly deserializes objects from the file."""
        obj = BaseModel()
        key = f"BaseModel.{obj.id}"
        self.storage.new(obj)
        self.storage.save()

        # Clear in-memory storage and reload from file
        FileStorage._FileStorage__objects.clear()
        self.storage.reload()

        self.assertIn(key, FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key]["id"], obj.id)

    def test_all_returns_objects(self):
        """Test that all returns the correct objects dictionary."""
        obj = BaseModel()
        self.storage.new(obj)
        all_objects = self.storage.all()

        key = f"BaseModel.{obj.id}"
        self.assertIn(key, all_objects)
        self.assertEqual(all_objects[key].id, obj.id)

    def test_empty_reload(self):
        """Test that reload works correctly with an empty file."""
        self.storage.save()
        self.storage.reload()
        self.assertEqual(self.storage._FileStorage__objects, {})

    def test_file_path(self):
        assert self.storage._FileStorage__file_path ==\
            self.file_path, "File path not set correctly"

    def test_explicit_objects(self):
        # Create a new object and save it
        obj = BaseModel(id="123", name="Test Object")
        self.storage.new(obj)
        self.storage.save()

        # Ensure object is in __objects
        self.assertIn("BaseModel.123", self.storage._FileStorage__objects)
        self.assertEqual(
            self.storage._FileStorage__objects["BaseModel.123"], obj.to_dict())


if __name__ == "__main__":
    unittest.main()
