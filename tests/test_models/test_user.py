#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the Review class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
import unittest
import time
from unittest.mock import patch
from datetime import datetime
from models.user import User
from models.base_model import BaseModel
from models import storage


class TestUser(unittest.TestCase):
    """Unit tests for the User class."""

    def test_instance_creation(self):
        """Test for creating an instance of the User class."""
        user = User()
        self.assertIsInstance(user, User)

    def test_inheritance_from_basemodel(self):
        """Test that User class correctly inherits from BaseModel."""
        user = User()
        self.assertTrue(issubclass(user.__class__, BaseModel))

    def test_class_attributes(self):
        """Test that class attributes are initialized correctly."""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertTrue(hasattr(user, "password"))
        self.assertTrue(hasattr(user, "first_name"))
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_email_attribute(self):
        """Test the email attribute of the User class."""
        user = User(email="test@example.com")
        self.assertEqual(user.email, "test@example.com")

    def test_password_attribute(self):
        """Test the password attribute of the User class."""
        user = User(password="password123")
        self.assertEqual(user.password, "password123")

    def test_first_name_attribute(self):
        """Test the first_name attribute of the User class."""
        user = User(first_name="John")
        self.assertEqual(user.first_name, "John")

    def test_last_name_attribute(self):
        """Test the last_name attribute of the User class."""
        user = User(last_name="Doe")
        self.assertEqual(user.last_name, "Doe")

    def test_create_user_with_kwargs(self):
        """Test creating a User instance with kwargs."""
        kwargs = {
            "email": "user@example.com",
            "password": "password123",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        user = User(**kwargs)
        self.assertEqual(user.email, kwargs["email"])
        self.assertEqual(user.password, kwargs["password"])
        self.assertEqual(user.first_name, kwargs["first_name"])
        self.assertEqual(user.last_name, kwargs["last_name"])
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_user_email(self):
        """Test the email attribute of the User class."""
        user = User(email="user@example.com")
        self.assertEqual(user.email, "user@example.com")

    def test_user_password(self):
        """Test the password attribute of the User class."""
        user = User(password="password123")
        self.assertEqual(user.password, "password123")

    def test_user_first_name(self):
        """Test the first_name attribute of the User class."""
        user = User(first_name="John")
        self.assertEqual(user.first_name, "John")

    def test_user_last_name(self):
        """Test the last_name attribute of the User class."""
        user = User(last_name="Doe")
        self.assertEqual(user.last_name, "Doe")

    def test_user_attributes(self):
        """Test User attributes."""
        obj = User()
        self.assertTrue(hasattr(obj, "email"))
        self.assertTrue(hasattr(obj, "password"))
        self.assertTrue(hasattr(obj, "first_name"))
        self.assertTrue(hasattr(obj, "last_name"))


class TestBaseModelSave(unittest.TestCase):
    """
    Test class to verify the save functionality of BaseModel.
    """

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    @patch("models.storage.save")
    def test_save_updates_updated_at(self, mock_save):
        """
        Test that calling save updates the 'updated_at' attribute.
        """
        user = User()
        old_updated_at = user.updated_at
        time.sleep(5)
        user.save()
        self.assertNotEqual(user.updated_at, old_updated_at)
        self.assertTrue(user.updated_at > old_updated_at)

    @patch("models.storage.save")
    def test_save_calls_storage_save(self, mock_save):
        """
        Test that save calls the storage's save method.
        """
        user = User()
        user.save()
        mock_save.assert_called_once()

    @patch('models.storage.new')
    @patch('models.storage.save')
    def test_user_save(self, mock_save, mock_new):
        """Test the save method of the User class."""
        user = User(email="user@example.com", password="password123")

        # Check if the save method is called on the storage engine
        user.save()
        # Ensure 'new' method was called
        mock_new.assert_called_once_with(user)
        mock_save.assert_called_once()  # Ensure 'save' method was called


if __name__ == '__main__':
    unittest.main()
