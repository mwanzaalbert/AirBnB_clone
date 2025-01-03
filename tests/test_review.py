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
import time
import unittest
from datetime import datetime
from models.review import Review
from models import storage


class TestReview(unittest.TestCase):
    """Unit tests for the Review class."""

    def setUp(self):
        """Set up test cases."""
        self.review = Review()

        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        del self.review

        storage._FileStorage__objects.clear()

    def test_instance_creation(self):
        """
        Test that a Review instance is created and inherits from BaseModel.
        """
        self.assertIsInstance(self.review, Review)
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))

    def test_default_attributes(self):
        """Test the default attributes of a Review instance."""
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_review_attributes(self):
        """Test Review attributes."""
        obj = Review()
        self.assertTrue(hasattr(obj, "place_id"))
        self.assertTrue(hasattr(obj, "user_id"))
        self.assertTrue(hasattr(obj, "text"))

    def test_attribute_assignment(self):
        """Test that attributes can be assigned correctly."""
        self.review.place_id = "place_123"
        self.review.user_id = "user_456"
        self.review.text = "Great place!"

        self.assertEqual(self.review.place_id, "place_123")
        self.assertEqual(self.review.user_id, "user_456")
        self.assertEqual(self.review.text, "Great place!")

    def test_kwargs_initialization(self):
        """Test initialization of a Review instance with keyword arguments."""
        data = {
            "id": "unique-id",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-02T12:00:00",
            "place_id": "place_789",
            "user_id": "user_987",
            "text": "Amazing experience!"
        }

        review = Review(**data)

        self.assertEqual(review.id, "unique-id")
        self.assertEqual(review.created_at,
                         datetime.fromisoformat("2025-01-01T12:00:00"))
        self.assertEqual(review.updated_at,
                         datetime.fromisoformat("2025-01-02T12:00:00"))
        self.assertEqual(review.place_id, "place_789")
        self.assertEqual(review.user_id, "user_987")
        self.assertEqual(review.text, "Amazing experience!")

    def test_save_method(self):
        """Test the save method to update the updated_at attribute."""
        old_updated_at = self.review.updated_at
        time.sleep(5)
        self.review.save()
        self.assertNotEqual(self.review.updated_at, old_updated_at)
        self.assertTrue(self.review.updated_at > old_updated_at)

    def test_str_representation(self):
        """Test the string representation of a Review instance."""
        string_rep = str(self.review)
        self.assertIn("Review", string_rep)
        self.assertIn("id", string_rep)
        self.assertIn("created_at", string_rep)
        self.assertIn("updated_at", string_rep)


if __name__ == "__main__":
    unittest.main()
