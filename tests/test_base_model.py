#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the BaseModel class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
import json
import time
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models import storage
from unittest.mock import patch
import uuid


class TestBaseModelAttributes(unittest.TestCase):
    """
    Test class to verify the attributes of the BaseModel class.
    """

    def setUp(self):
        """
        Set up test cases by creating a BaseModel instance.
        """
        self.model = BaseModel()

        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.model

        storage._FileStorage__objects.clear()

    def test_id_is_string(self):
        """
        Test if the 'id' attribute is a string and a valid UUID.
        """
        self.assertIsInstance(self.model.id, str)
        try:
            uuid_obj = uuid.UUID(self.model.id, version=4)
            self.assertEqual(str(uuid_obj), self.model.id)
        except ValueError:
            self.fail("id is not a valid UUID")

    def test_created_at_is_datetime(self):
        """
        Test if the 'created_at' attribute is a datetime object.
        """
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test if the 'updated_at' attribute is a datetime object.
        """
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_created_at_and_updated_at_equal_on_init(self):
        """
        Test if 'created_at' and 'updated_at' are equal upon initialization.
        """
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_to_dict_contains_correct_attributes(self):
        """
        Test if the 'to_dict' method returns the correct attributes.
        """
        model_dict = self.model.to_dict()
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('__class__', model_dict)

    def test_to_dict_datetime_format(self):
        """
        Test if 'created_at' and 'updated_at' are in ISO 8601 format in
        'to_dict'.
        """
        model_dict = self.model.to_dict()
        try:
            datetime.fromisoformat(model_dict['created_at'])
            datetime.fromisoformat(model_dict['updated_at'])
        except ValueError:
            self.fail("created_at or updated_at is not in ISO format")


class TestBaseModelInstantiation(unittest.TestCase):
    """
    Test class to verify the instantiation of BaseModel.
    """

    def test_no_args_instantiation(self):
        """
        Test BaseModel instantiation with no arguments.
        """
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_kwargs_instantiation(self):
        """
        Test BaseModel instantiation with keyword arguments.
        """
        kwargs = {
            "id": "1234",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.id, "1234")
        self.assertEqual(model.created_at.isoformat(), kwargs["created_at"])
        self.assertEqual(model.updated_at.isoformat(), kwargs["updated_at"])

    def test_kwargs_ignores_class_key(self):
        """
        Test BaseModel instantiation ignores '__class__' key in kwargs.
        """
        kwargs = {
            "id": "5678",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "__class__": "BaseModel"
        }
        model = BaseModel(**kwargs)
        self.assertNotIn("__class__", model.__dict__)
        self.assertEqual(model.id, "5678")

    def test_basemodel_attributes(self):
        """Test BaseModel attributes."""
        obj = BaseModel()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))


class TestBaseModelSave(unittest.TestCase):
    """
    Test class to verify the save functionality of BaseModel.
    """

    def setUp(self):
        """Set up test environment. Clears the storage and removes file.json
        if it exists."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    @patch("models.storage.save")
    def test_save_updates_updated_at(self, mock_save):
        """
        Test that calling save updates the 'updated_at' attribute.
        """
        model = BaseModel()
        old_updated_at = model.updated_at
        time.sleep(5)
        model.save()
        self.assertNotEqual(model.updated_at, old_updated_at)
        self.assertTrue(model.updated_at > old_updated_at)

    @patch("models.storage.save")
    def test_save_calls_storage_save(self, mock_save):
        """
        Test that save calls the storage's save method.
        """
        model = BaseModel()
        model.save()
        mock_save.assert_called_once()


class TestBaseModelStr(unittest.TestCase):
    """
    Test class to verify the string representation of BaseModel.
    """

    def test_str_representation(self):
        """
        Test the __str__ method for proper string representation.
        """
        model = BaseModel()
        expected_str = f"[{model.__class__.__name__}] ({model.id}) " +\
            f"{model.__dict__}"
        self.assertEqual(str(model), expected_str)


class TestBaseModelFileSaving(unittest.TestCase):
    """Test cases for saving BaseModel objects to file.json."""

    def setUp(self):
        """Set up test environment. Clears the storage and removes file.json
        if it exists."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def tearDown(self):
        """Clean up after tests by removing file.json if it exists."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def test_save_to_file(self):
        """Test that a BaseModel object is correctly saved to file.json."""
        obj = BaseModel()
        obj.name = "TestObject"
        obj.number = 123
        obj.save()

        # Verify that file.json exists
        self.assertTrue(os.path.exists(self.file_path))

        # Verify content of file.json
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        key = f"BaseModel.{obj.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]['name'], "TestObject")
        self.assertEqual(data[key]['number'], 123)
        self.assertEqual(data[key]['id'], obj.id)

    def test_reload_from_file(self):
        """
        Test that objects saved in file.json can be reloaded into storage.
        """
        obj = BaseModel()
        obj.name = "ReloadTest"
        obj.number = 456
        obj.save()

        # Reload storage
        storage.reload()

        # Verify that the object is reloaded correctly
        key = f"BaseModel.{obj.id}"
        reloaded_objects = storage.all()
        self.assertIn(key, reloaded_objects)
        reloaded_obj = reloaded_objects[key]

        self.assertEqual(reloaded_obj.name, "ReloadTest")
        self.assertEqual(reloaded_obj.number, 456)
        self.assertEqual(reloaded_obj.id, obj.id)


class TestBaseModelToDict(unittest.TestCase):
    """Test cases for the to_dict method of BaseModel."""

    def test_to_dict_contains_all_attributes(self):
        """Test that to_dict contains all instance attributes."""
        obj = BaseModel()
        obj.name = "TestObject"
        obj.number = 123
        obj_dict = obj.to_dict()

        # Check that all attributes are in the dictionary
        self.assertIn("id", obj_dict)
        self.assertIn("created_at", obj_dict)
        self.assertIn("updated_at", obj_dict)
        self.assertIn("name", obj_dict)
        self.assertIn("number", obj_dict)

        # Check values
        self.assertEqual(obj_dict["name"], "TestObject")
        self.assertEqual(obj_dict["number"], 123)
        self.assertEqual(obj_dict["id"], obj.id)

    def test_to_dict_contains_class_name(self):
        """
        Test that to_dict contains the __class__ key with the correct value.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()

        self.assertIn("__class__", obj_dict)
        self.assertEqual(obj_dict["__class__"], "BaseModel")

    def test_to_dict_datetime_format(self):
        """
        Test that created_at and updated_at are in ISO 8601 string format.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()

        # Check that created_at and updated_at are strings in ISO format
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)

        # Verify that ISO format is valid
        created_at = datetime.fromisoformat(obj_dict["created_at"])
        updated_at = datetime.fromisoformat(obj_dict["updated_at"])

        self.assertEqual(created_at, obj.created_at)
        self.assertEqual(updated_at, obj.updated_at)

    def test_to_dict_independence(self):
        """Test that modifying the returned dictionary does not affect the
        instance."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        obj_dict["name"] = "Modified"

        self.assertNotIn("name", obj.__dict__)


if __name__ == '__main__':
    unittest.main()
