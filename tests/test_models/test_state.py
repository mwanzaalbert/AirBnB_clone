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
from datetime import datetime
from unittest.mock import patch, MagicMock
from models.state import State
from models import storage


class TestState(unittest.TestCase):
    """
    Test cases for the State class.
    """

    def setUp(self):
        """Set up test environment before each test."""
        self.state = State()
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.state

        storage._FileStorage__objects.clear()

    def test_initialization_no_kwargs(self):
        """Test initialization without kwargs."""
        self.assertEqual(self.state.name, "")
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)

    def test_initialization_with_kwargs(self):
        """Test initialization with kwargs."""
        kwargs = {
            "id": "1234",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": "New York"
        }
        state = State(**kwargs)
        self.assertEqual(state.id, "1234")
        self.assertEqual(state.name, "New York")
        self.assertIsInstance(state.created_at, datetime)
        self.assertIsInstance(state.updated_at, datetime)

    def test_state_attributes(self):
        """Test State attributes."""
        obj = State()
        self.assertTrue(hasattr(obj, "name"))

    @patch("models.storage.new")
    def test_storage_new_called_on_init(self, mock_new):
        """Test if storage.new is called when a State is initialized."""
        state = State()
        mock_new.assert_called_once_with(state)

    def test_name_attribute(self):
        """Test the name attribute of State."""
        self.state.name = "California"
        self.assertEqual(self.state.name, "California")

    def test_save_updates_updated_at(self):
        """Test that save method updates updated_at."""
        old_updated_at = self.state.updated_at
        time.sleep(5)
        self.state.save()
        self.assertNotEqual(self.state.updated_at, old_updated_at)

    @patch("models.storage.save")
    def test_save_calls_storage_save(self, mock_save):
        """Test that save method calls storage.save."""
        self.state.save()
        mock_save.assert_called_once()

    def test_to_dict_contains_expected_keys(self):
        """Test that to_dict contains expected keys."""
        state_dict = self.state.to_dict()
        expected_keys = ["id", "created_at", "updated_at", "name", "__class__"]
        for key in expected_keys:
            self.assertIn(key, state_dict)

    def test_to_dict_datetime_format(self):
        """
        Test that created_at and updated_at are formatted correctly in to_dict.
        """
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict["created_at"],
                         self.state.created_at.isoformat())
        self.assertEqual(state_dict["updated_at"],
                         self.state.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
