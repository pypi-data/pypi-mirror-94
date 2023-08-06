import unittest
import os
from pathlib import Path
import shutil

from equit_ease.parser.parse import UserConfigParser

user_home_dir = str(Path.home())
equit_ease_dir = os.path.join(user_home_dir, ".equit_ease")
os_agnostic_path = Path(equit_ease_dir)
lists_file_path = Path(os.path.join(equit_ease_dir, "lists"))


def remove_equit_ease_dir():
    """remove the directory structure for unit tests."""
    shutil.rmtree(equit_ease_dir)


def setup_equit_ease_dir():
    """create the directory structure for unit tests."""
    os_agnostic_path.mkdir()
    with open(lists_file_path, "w") as f:
        f.writelines(["[Test]\n", "equity_names = CRM,AAPL,GME,MSFT,AXP"])


class TestUserConfigParser(unittest.TestCase):
    """Testing methods from the UserConfigParser class."""

    if os.path.exists(lists_file_path):
        remove_equit_ease_dir()
        setup_equit_ease_dir()
    else:
        setup_equit_ease_dir()

    def setUp(self):
        self.list_name = "Test"
        self.list_file_contents = open(lists_file_path, "r").read().splitlines()
        self.parser = UserConfigParser(self.list_name, self.list_file_contents)
        self.equities, _ = self.parser.format_equity_lists()

    def tearDown(self):
        self.list_name = None
        self.list_file_contents = None
        self.parser = UserConfigParser
        self.equities = None

    def test_equities_getter(self):
        """
        test case #1 for the .equities property.

        Expected behavior: `equities` is initially set to None,
        and is updated based on user input throughout the application.
        Once it is set to a value with the setter, that should be
        reflected via the getter.

        This test checks to see that the initial value is set to None and
        validly updates
        """
        self.parser.equities = None

        self.assertTrue(  # test None
            isinstance(self.parser.equities, list)
            if self.parser.equities is not None
            else self.parser.equities is None
        )

    def test_equities_setter(self):
        """
        test case #2 for `equities` property.

        Expected behavior: see test case #1.

        This test checks to see that the equities
        property is correctly updated and set to a
        list.
        """
        self.parser.equities, _ = self.parser.format_equity_lists()

        self.assertTrue(  # test list
            isinstance(self.parser.equities, list)
            if self.parser.equities is not None
            else self.parser.equities is None
        )

    def test_list_name_getter(self):
        """
        test case #1 for `list_name` property.

        Expected behavior: the list name should initially
        be set to "Test"
        """
        self.assertTrue(self.parser.list_name == "Test")

    def test_list_name_setter(self):
        """
        test case #2 for `list_name` property.

        Expected behavior: see test case #1.

        This test checks to see that the list_name
        is correctly updated when the setter is called.
        """
        self.assertTrue(self.parser.list_name == "Test")

        self.parser.list_name = "New List"

        self.assertTrue(self.parser.list_name == "New List")

    def test_format_equity_lists(self):
        """
        test case #1 for format_equity_lists().

        Expected behavior: returns a tuple containing
        a list of all user-configured lists and a string
        of comma-separated user-configured list names.
        """
        formatted_list_names = self.parser.format_equity_lists()

        self.assertIsInstance(formatted_list_names[0], list)

        self.assertTrue(formatted_list_names[0] == ["Test"])

        self.assertTrue(formatted_list_names[1] == "Test")

    def test_find_match(self):
        """
        test case #1 for find_match().

        Expected behavior: given a list_name, searches for
        the first match and returns the equities assigned to
        that list name. Returns them as a list.
        """
        equities = self.parser.find_match()

        self.assertEqual(
            equities, ["CRM","AAPL","GME","MSFT","AXP"]
        )
