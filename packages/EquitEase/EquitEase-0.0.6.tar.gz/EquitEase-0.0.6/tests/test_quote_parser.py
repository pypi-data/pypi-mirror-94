import dataclasses
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants
import unittest
import json
import os

from equit_ease.parser.parse import QuoteParser

__status__ = "up_to_date"


def read_quote_fixture(fpath: str):
    fixture_file_path = os.path.join(os.path.dirname(__file__), fpath)
    with open(fixture_file_path, "r") as quote_fixture:
        data = json.loads(quote_fixture.read())
    return data


class TestQuoteParserMethods(unittest.TestCase):
    """Testing methods from the QuoteParser class."""

    def setUp(self):
        self.equity = "Apple"
        self.data_fixture = read_quote_fixture("fixtures/quote.json")
        self.errant_data_fixture = read_quote_fixture("fixtures/quote-errant.json")
        self.parser = QuoteParser(self.equity, self.data_fixture)

    def tearDown(self):
        self.ticker_to_search = None
        self.data_fixture = None
        self.parser = QuoteParser

    def test_extract_equity_meta_data_instance_type(self):
        """
        test extract_equity_meta_data() internal method #1 -> pass.

        check that the response from extract_equity_meta_data() is a
        EquityMeta dataclass instance with the expected field names.
        """
        equity_meta = self.parser.extract_equity_meta_data()
        received_field_names = [field.name for field in dataclasses.fields(equity_meta)]
        expected_field_names = [field.name for field in dataclasses.fields(EquityMeta)]

        self.assertIsInstance(equity_meta, EquityMeta)
        self.assertEqual(received_field_names, expected_field_names)

    def test_extract_equity_metadata_validity(self):
        """
        test extract_equity_meta_data() method #2 -> pass.

        this time, checking for the validity of the data that is
        mapped from JSON -> the dataclass.
        """
        equity_meta_as_dict = dataclasses.asdict(self.parser.extract_equity_meta_data())
        quote_fixture = read_quote_fixture("fixtures/quote.json")
        data_for_validation = quote_fixture["quoteResponse"]["result"][0]
        column_mappings = Constants.yahoo_finance_column_mappings

        for dataclass_key, json_data_key in column_mappings.items():
            self.assertEqual(
                equity_meta_as_dict[dataclass_key], data_for_validation[json_data_key]
            )

    def test_extract_equity_metadata_errant(self):
        """
        test extract_equity_meta_data() method #3 -> pass.

        If a key is missing from the JSON object, it's value should be
        N/A. In the errant fixture (fixtures/quote-errant.json), the
        ``regularMarketOpen`` key has been removed. Therefore, the dataclass
        should have the open field == 'N/A'.
        """

        parser = QuoteParser(self.equity, self.errant_data_fixture)
        equity_meta = parser.extract_equity_meta_data()
        self.assertTrue(equity_meta.open == "N/A")
