import unittest

from equit_ease.parser.parse import Parser

__status__ = "up_to_date"


class TestParserMethods(unittest.TestCase):
    def setUp(self):
        """set-up before each test is run."""
        self.ticker_to_search = "tsla"
        self.data_fixture = {"one": "first key", "two": None}
        self.parser = Parser(self.ticker_to_search, self.data_fixture)

    def tearDown(self):
        self.ticker_to_search = None
        self.data_fixture = None
        self.parser = Parser

    def test_extract_data_from_pass(self):
        """test case #1 for _extract_data_from() in parser/parse.py -> pass"""

        extracted_data_one = self.parser._extract_data_from(
            self.data_fixture, "invalid_key"
        )
        extracted_data_two = self.parser._extract_data_from(self.data_fixture, "one")
        extracted_data_three = self.parser._extract_data_from(self.data_fixture, "two")

        self.assertEqual(
            extracted_data_one, "N/A"
        )  # returns N/A for keys that don't exist in the data struct
        self.assertEqual(extracted_data_two, "first key")
        self.assertIsNone(extracted_data_three)

    def test_extract_data_from_pass_empty(self):
        """test case #2 for _extract_data_from() in parser/parse.py -> pass"""

        extracted_data_one = self.parser._extract_data_from(
            self.data_fixture, "invalid_key"
        )
        extracted_data_two = self.parser._extract_data_from(
            self.data_fixture, "another_invalid_key"
        )

        self.assertEquals(extracted_data_one, "N/A")
        self.assertEquals(extracted_data_two, "N/A")

    def test_build_dict_repr_pass(self):
        """test case #1 for _build_dict_repr in parser/parse.py -> pass."""

        keys_to_extract_one = ["one", "two", "three"]
        keys_to_extract_two = ["abc", "xyz", "123"]
        keys_to_extract_three = [123, 456, 789]

        dict_repr_one = self.parser._build_dict_repr(
            keys_to_extract_one, self.data_fixture
        )
        dict_repr_two = self.parser._build_dict_repr(
            keys_to_extract_two, self.data_fixture
        )
        dict_repr_three = self.parser._build_dict_repr(
            keys_to_extract_three, self.data_fixture
        )

        self.assertTrue(("first key" and "N/A" and None) in set(dict_repr_one.values()))
        self.assertTrue(len(set(dict_repr_two.values())) == 1)
        self.assertTrue(len(set(dict_repr_three.values())) == 1)
