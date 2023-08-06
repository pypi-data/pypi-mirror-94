import json
from logging import ERROR
import os

from equit_ease.parser.parse import ChartParser
import unittest


def read_quote_fixture(fpath: str):
    fixture_file_path = os.path.join(os.path.dirname(__file__), fpath)
    with open(fixture_file_path, "r") as quote_fixture:
        data = json.loads(quote_fixture.read())
    return data


class TestChartParserMethods(unittest.TestCase):
    """testing methods from the ChartParser class."""

    def setUp(self):
        self.equity = "Apple"
        self.data_fixture = read_quote_fixture("fixtures/chart.json")
        self.errant_data_fixture = read_quote_fixture("fixtures/chart-errant.json")
        self.parser = ChartParser(self.equity, self.data_fixture)

    def tearDown(self):
        self.ticker_to_search = None
        self.data_fixture = None
        self.parser = ChartParser

    def test_extract_equity_chart_data_keys(self):
        """
        test extract_equity_chart_data() #1 -> pass.

        check that the response from extract_equity_chart_data() is a
        tuple containing the following keys. Additionally, for each key,
        check that non-standardized values are not equal to `chart_data`
        and standardized values are equal to `chart_data`.
        )
        """
        keys = ("low", "high", "open", "close", "volume")
        chart_data = self.parser.extract_equity_chart_data()

        for i, key in enumerate(keys):
            filtered_chart_data = self.data_fixture["chart"]["result"][0]["indicators"][
                "quote"
            ][0][key]

            # data is not standardized, so None values appear
            self.assertNotEqual(filtered_chart_data, chart_data[i])
            # data is standardized
            self.assertEqual(
                self.parser.standardize(filtered_chart_data), chart_data[i]
            )

    def test_extract_equity_chart_data_length(self):
        """
        test extract_equity_chart_data() #2 -> pass.

        check that the length of all values returned from
        extract_equity_chart_data() are equal.

        This test is more concerned with confirming a key
        assumption underlying the application: the length of
        open, close, bid, ask, etc... should all be the same.
        """
        keys = ("low", "high", "open", "close", "volume")

        responses = dict()

        for key in keys:
            filtered_chart_data = self.data_fixture["chart"]["result"][0]["indicators"][
                "quote"
            ][0][key]

            responses[key] = filtered_chart_data

        self.assertTrue(
            len(responses["low"])
            == len(responses["high"])
            == len(responses["open"])
            == len(responses["close"])
            == len(responses["volume"])
        )

    def test_extract_equity_chart_data_errant(self):
        """
        test case #3 for extract_equity_chart_data() with errant fixture -> pass.

        Using the chart-errant.json fixture, test the functionality
        given unequal list lengths for the 'low', 'high', ..., etc.

        No error should be raised.
        """
        keys = ("low", "high", "open", "close", "volume")

        responses = dict()

        for key in keys:
            filtered_chart_data = self.errant_data_fixture["chart"]["result"][0][
                "indicators"
            ]["quote"][0][key]

            responses[key] = filtered_chart_data

        self.assertFalse(
            len(responses["low"])
            == len(responses["high"])
            == len(responses["open"])
            == len(responses["close"])
            == len(responses["volume"])
        )

    def test_standardize_pass(self):
        """
        test case #1 for standardize() -> pass.

        Appropriate params are passed to the function,
        resulting in expected results.
        """
        test_data = [0, None, 0, 1, 2]
        average = sum([item for item in test_data if item != None]) / len(
            [item for item in test_data if item != None]
        )
        clean_test_data = [0, average, 0, 1, 2]

        standardized_data = self.parser.standardize(test_data)
        index_of_average = standardized_data.index(average)

        self.assertEqual(standardized_data, clean_test_data)

        self.assertEqual(index_of_average, 1)

    def test_standardize_fail(self):
        """
        test case #2 for standardize() -> fail.

        Params that cause errors are passed, resulting in
        ``Error``
        """
        test_data_one = [None, None, None, None]
        test_data_two = [0, 0, 0, 0]
        test_data_three = ["0", "0", "0", "0"]

        with self.assertRaises(ZeroDivisionError):
            self.parser.standardize(test_data_one)

        # should be unchanged
        self.assertEqual(self.parser.standardize(test_data_two), test_data_two)

        with self.assertRaises(TypeError):
            self.parser.standardize(test_data_three)
