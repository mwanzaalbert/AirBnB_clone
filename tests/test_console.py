#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suite for the HBNBCommand class.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import os
from io import StringIO
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models import storage

classes = ["BaseModel", "User",
           "State", "City", "Amenity",
           "Place", "Review"
           ]


class TestConsole(unittest.TestCase):
    """Test cases for the HBNBCommand class."""

    def test_quit_command(self):
        """Test the quit command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_eof_command(self):
        """Test the EOF command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_empty_line(self):
        """Test empty line input."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))

    def test_help_command(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("help")
            self.assertIn("Documented commands", output.getvalue())


class TestHBNBCommandEmptyLine(unittest.TestCase):
    """Unittest for the emptyline method in HBNBCommand."""

    def setUp(self):
        """Set up the test environment."""
        self.console = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_line(self, mock_stdout):
        """Test that empty line does nothing."""
        # Simulate pressing ENTER with an empty line
        self.console.onecmd("")
        self.assertEqual(mock_stdout.getvalue(), "")  # No output expected

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_line_with_spaces(self, mock_stdout):
        """Test that a line with only spaces does nothing."""
        # Simulate pressing ENTER with a line of spaces
        self.console.onecmd("   ")
        self.assertEqual(mock_stdout.getvalue(), "")  # No output expected


class TestConsoleCreate(unittest.TestCase):
    """Test cases for the create command."""

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

    def test_create_each_class(self):
        """Test create command for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                self.assertRegex(output.getvalue().strip(), r'^[0-9a-f-]{36}$')

    def test_create_invalid_class(self):
        """Test create with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("create FakeClass")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")


class TestConsoleShow(unittest.TestCase):
    """Test cases for the show command."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def test_show_valid_instance(self):
        """Test show with a valid instance."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as show_output:
                    HBNBCommand().onecmd(f"show {cls} {instance_id}")
                    self.assertIn(instance_id, show_output.getvalue().strip())

    def test_show_invalid_class(self):
        """Test show with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show FakeClass 1234")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_show_missing_id(self):
        """Test show with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"show {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_show_nonexistent_id(self):
        """Test show with a nonexistent ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"show {cls} 1234")
                self.assertEqual(output.getvalue().strip(),
                                 "** no instance found **")


class TestConsoleUpdate(unittest.TestCase):
    """Test cases for the show command."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def test_update_valid_instance(self):
        """Test update command for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(
                        f"update {cls} {instance_id} author 'Albert'")
                    self.assertEqual(update_output.getvalue().strip(), "")

    def test_update_invalid_class(self):
        """Test show with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update FakeClass 1234 author 'Albert'")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_update_nonexistent_id(self):
        """Test show with a nonexistent ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"update {cls} 1234 author 'Albert'")
                self.assertEqual(output.getvalue().strip(),
                                 "** no instance found **")

    def test_update_missing_id(self):
        """Test show with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"update {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_update_missing_attr_name(self):
        """Test show with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"update {cls} 1234")
                self.assertEqual(output.getvalue().strip(),
                                 "** attribute name missing **")

    def test_update_missing_attr_value(self):
        """Test show with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"update {cls} 1234 author")
                self.assertEqual(output.getvalue().strip(),
                                 "** value missing **")


class TestConsoleDestroy(unittest.TestCase):
    """Test cases for the destroy command."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def test_destroy_valid_instance(self):
        """Test destroy with a valid instance."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    HBNBCommand().onecmd(f"destroy {cls} {instance_id}")
                    self.assertEqual(destroy_output.getvalue().strip(), "")

    def test_destroy_invalid_class(self):
        """Test destroy with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy FakeClass 1234")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"destroy {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_destroy_nonexistent_id(self):
        """Test destroy with a nonexistent ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"destroy {cls} 1234")
                self.assertEqual(output.getvalue().strip(),
                                 "** no instance found **")
    #


class TestConsoleAll(unittest.TestCase):
    """Test cases for the all command."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.file_path = "file.json"

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def tearDown(self):
        """Clean up after each test by removing the test file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage._FileStorage__objects.clear()

    def test_all(self):
        """Test all command without class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all")
            self.assertIsInstance(output.getvalue().strip(), str)

    def test_all_with_class(self):
        """Test all command with a valid class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"all {cls}")
                self.assertIsInstance(output.getvalue().strip(), str)

    def test_all_invalid_class(self):
        """Test all command with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all FakeClass")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")


class TestConsoleAdvanced(unittest.TestCase):
    """Test cases for count, show, and update commands for each class."""

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

    def test_count(self):
        """Test count command for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as count_output:
                    HBNBCommand().onecmd(f"{cls}.count()")
                    self.assertRegex(count_output.getvalue().strip(), r'^\d+$')

    def test_show(self):
        """Test show command for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as show_output:
                    HBNBCommand().onecmd(f"{cls}.show({instance_id})")
                    self.assertIn(instance_id, show_output.getvalue().strip())

    def test_show_nonexistent(self):
        """Test show command with nonexistent ID for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as show_output:
                    HBNBCommand().onecmd(f"{cls}.show(1234)")
                    self.assertEqual(show_output.getvalue().strip(),
                                     "** no instance found **")

    def test_all(self):
        """Test all command without class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"{cls}.all()")
                self.assertIsInstance(output.getvalue().strip(), str)
                self.assertEqual(output.getvalue().strip(), '[]')

        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()

                all_instance_entry = f"[{cls}] ({instance_id})"
                with patch('sys.stdout', new=StringIO()) as all_output:
                    HBNBCommand().onecmd(f"{cls}.all()")
                    self.assertIn(all_instance_entry,
                                  all_output.getvalue().strip())

    def test_all_invalid_class(self):
        """Test all command with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("FakeClass.all()")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_update(self):
        """Test update command for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(
                        f"{cls}.update({instance_id}, attr_name, 'value')")
                    self.assertEqual(update_output.getvalue().strip(), "")

    def test_update_nonexistent(self):
        """Test update command with nonexistent ID for each class."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as output:
                    HBNBCommand().onecmd(
                        f"{cls}.update(1234, attr_name, 'value')")
                    self.assertEqual(output.getvalue().strip(),
                                     "** no instance found **")

    def test_destroy_valid_instance(self):
        """Test destroy with a valid instance."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    HBNBCommand().onecmd(f"{cls}.destroy({instance_id})")
                    self.assertEqual(destroy_output.getvalue().strip(), "")

    def test_destroy_invalid_class(self):
        """Test destroy with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("FakeClass.destroy(1234)")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with a missing ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"{cls}.destroy()")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_destroy_nonexistent_id(self):
        """Test destroy with a nonexistent ID."""
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    HBNBCommand().onecmd(f"{cls}.destroy(1234)")
                    self.assertEqual(destroy_output.getvalue().strip(),
                                     "** no instance found **")


class TestConsoleShowUpdateDict(unittest.TestCase):
    """Test cases for show and update commands with dictionary input for each
    class."""

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

    def test_show_with_dict(self):
        """
        Test show command when a dictionary is used in update for each class.
        """
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(
                        f"{cls}.update({instance_id}, {{'author': 'Albert'}})")
                    self.assertEqual(update_output.getvalue().strip(), "")
                with patch('sys.stdout', new=StringIO()) as show_output:
                    HBNBCommand().onecmd(f"{cls}.show({instance_id})")
                    self.assertIn("'author': 'Albert'",
                                  show_output.getvalue().strip())

    def test_update_with_dict_nonexistent_id(self):
        """
        Test update command with dictionary for nonexistent ID in each class.
        """
        for cls in classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as output:
                    HBNBCommand().onecmd(
                        f"{cls}.update(1234, {{'author': 'Albert'}})")
                    self.assertEqual(output.getvalue().strip(),
                                     "** no instance found **")


if __name__ == "__main__":
    unittest.main()
