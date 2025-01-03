#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Console module for HBNBCommand.

HBNBCommand - a command interpreter for managing models and their storage.

This module allows interaction with a storage engine by providing commands to
create, retrieve,update, and delete objects of various classes.
"""
__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-01-03"
__version__ = "1.1"

import ast
import cmd
import shlex
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage

# Dictionary mapping class names to their respective class objects
class_models = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB."""
    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """Type Ctrl-D to exit the program
        """
        return True

    def do_create(self, line):
        """Create a new instance of a class.

        usage:
        ------
        create <class name>
        """
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        cls = args[0]
        if cls not in class_models:
            print("** class doesn't exist **")
            return

        # Create a new instance
        my_model = class_models[cls]()
        my_model.save()
        print(my_model.id)

    def do_show(self, line):
        """Show an object by class name and ID.

        usage:
        ------
        show <class name> <instance id>
        """
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        cls = args[0]
        if cls not in class_models:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        id = args[1].strip('\'" ')
        key = f"{cls}.{id}"

        data = storage.all()

        if key not in data:
            print("** no instance found **")
            return

        print(data[key])

    def do_destroy(self, line):
        """Show an object by class name and ID.

        usage:
        ------
        destroy <class name> <instance id>
        """
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        cls = args[0].strip('\'" ')
        if cls not in class_models:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        id = args[1].strip('\'" ')
        key = f"{cls}.{id}"

        data = storage.all()

        if key not in data:
            print("** no instance found **")
            return

        del storage._FileStorage__objects[key]

        storage.save()

    def do_all(self, line):
        """Display all instances of a class or all instances if no class is
        specified.

        Usage:
        ------
        all [<class name>]
        """
        args = line.split()

        cls = args[0].strip('\'" ') if args else None

        if cls is not None and cls not in class_models:
            print("** class doesn't exist **")
            return

        storage.reload()

        loaded_dict = storage._FileStorage__objects.copy()

        if cls is not None:
            data = [str({obj: key}) for obj,
                    key in loaded_dict.items() if obj.split('.')[0] == cls]
        else:
            data = [str({obj: key}) for obj,
                    key in loaded_dict.items()]

        print(data)

    def do_update(self, line):
        """Update an object's attribute.

        Usage:
        ------
        update <class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(line)[:4]

        if len(args) < 1:
            print("** class name missing **")
            return

        cls = args[0]
        if cls not in class_models:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        id = args[1].strip('\'" ')
        key = f"{cls}.{id}"
        attr_name = args[2].strip('\'" ')
        attr_value = args[3].strip('\'" ')  # Remove quotes

        data = storage.all()

        if key not in data:
            print("** no instance found **")
            return

        # Update the attribute
        obj = data[key]
        try:
            # Convert to appropriate type if possible
            attr_value = json.loads(attr_value)
        except (json.JSONDecodeError):
            pass  # Keep as string if evaluation fails

        finally:
            setattr(obj, attr_name, attr_value)

            obj.save()  # Save the updated object

    def default(self, line):
        """Handle unrecognized commands, including custom syntax for class
        methods.
        """
        if "." not in line:
            print(f"*** Unknown syntax: {line} ***")
            return

        class_method = line.split(".", 1)
        if len(class_method) != 2:
            print(f"*** Unknown syntax: {line} ***")
            return

        cls, method = class_method

        method = method.strip()

        data = storage.all()

        if cls not in class_models:
            print("** class doesn't exist **")
            return

        if method == "all()":
            cls_instances = [obj for key,
                             obj in data.items() if key.startswith(f"{cls}.")]

            print("[", end="")
            for index, obj in enumerate(cls_instances):
                if index < len(cls_instances) - 1:
                    print(obj, end=', ')
                else:
                    print(obj, end='')
            print("]")

        elif method == "count()":
            count = sum(1 for key in data if key.startswith(f"{cls}."))
            print(count)

        elif method.startswith("show(") and method.endswith(")"):
            # Extract ID from `show(<id>)`
            obj_id = method[5:-1].strip('\'" ')
            if not obj_id:
                print("** instance id missing **")
                return

            key = f"{cls}.{obj_id}"

            if key not in data:
                print("** no instance found **")
                return

            print(data[key])

        elif method.startswith("destroy(") and method.endswith(")"):
            # Extract ID from `destroy(<id>)`
            obj_id = method[8:-1].strip('\'" ')
            if not obj_id:
                print("** instance id missing **")
                return

            key = f"{cls}.{obj_id}"

            data = storage.all()

            if key not in data:
                print("** no instance found **")
                return

            del storage._FileStorage__objects[key]

            storage.save()  # Save changes to file

        elif method.startswith("update(") and method.endswith(")"):
            if any(char in method[7:-1] for char in "{}"):
                params = method[7:-1].split(", ", 1)
            else:
                params = method[7:-1].split(", ")

            if len(params) < 1:
                print("** instance id missing **")
                return

            if len(params) < 2:
                print("** attribute name missing **")
                return

            if len(params) < 3:
                if any(char in params[1] for char in "{}"):
                    obj_id, attr_or_dict = params[:2]

                    obj_id = obj_id.strip('\'" ')

                    key = f"{cls}.{obj_id}"
                    data = storage.all()

                    if key not in data:
                        print("** no instance found **")
                        return

                    # Update the attribute
                    obj = data[key]

                    # Handle dictionary representation
                    try:
                        # Safely evaluates Python dictionary-like strings
                        attr_dict = ast.literal_eval(attr_or_dict.strip())
                        if not isinstance(attr_dict, dict):
                            raise ValueError
                    except (SyntaxError, ValueError):
                        print("** invalid dictionary representation **")
                        return
                    else:
                        for attr_name, attr_value in attr_dict.items():
                            setattr(obj, attr_name, attr_value)

                        obj.save()  # Save the updated object
                        return
                else:
                    print("** value missing **")
                    return

            obj_id, attr_name, attr_value = params[:3]

            obj_id = obj_id.strip('\'" ')
            attr_name = attr_name.strip('\'" ')
            attr_value = attr_value.strip('\'" ')  # Remove quotes

            key = f"{cls}.{obj_id}"
            data = storage.all()

            if key not in data:
                print("** no instance found **")
                return

            # Update the attribute
            obj = data[key]
            try:
                # Convert to appropriate type if possible
                attr_value = json.loads(attr_value)
            except (json.JSONDecodeError):
                pass  # Keep as string if evaluation fails

            finally:
                setattr(obj, attr_name, attr_value)
                obj.save()  # Save the updated object

        else:
            print("*** Unknown syntax:", line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
