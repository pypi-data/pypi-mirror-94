import unittest
from requests.exceptions import HTTPError
import re

from equit_ease.reader.read import Reader
from equit_ease.utils.Constants import Constants

__status__ = "up-to-date"


class TestReaderMethods(unittest.TestCase):
    # test the methods defined for the Reader class.

    def setUp(self):
        """set-up before each test is run."""

        def set_up_reader_co(reader: Reader) -> Reader:
            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.build_equity_quote_url()
            reader.build_equity_chart_url()
            return reader

        def set_up_reader_tick(reader: Reader) -> Reader:
            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.build_equity_quote_url()
            reader.build_equity_chart_url()
            return reader

        self.company_name = "Apple"
        self.ticker_name = "CRM"
        self.reader_co = set_up_reader_co(Reader(self.company_name))
        self.reader_tick = set_up_reader_tick(Reader(self.ticker_name))

    def tearDown(self):
        self.company_name = None
        self.ticker_name = None
        self.reader_co = Reader
        self.reader_tick = Reader

    def test_build_equity_chart_url_pass(self):
        """test case #1 for build_equity_chart_url() in reader/read.py -> pass"""
        reader = self.reader_co

        full_url_one = Constants.yahoo_finance_base_chart_url + reader.ticker
        # builds the URL and sets it as a class instance(!!!) attribute
        _ = reader.build_equity_chart_url()
        self.assertEqual(reader.chart_base_url, full_url_one)

        extract_range = lambda url: re.search("range=(.*)", url)
        self.assertTrue(extract_range(reader.chart_one_year_url).group(1) == "1y")
        self.assertTrue(extract_range(reader.chart_six_months_url).group(1) == "6mo")
        self.assertTrue(extract_range(reader.chart_three_months_url).group(1) == "3mo")
        self.assertTrue(extract_range(reader.chart_one_month_url).group(1) == "1mo")
        self.assertTrue(extract_range(reader.chart_five_days_url).group(1) == "5d")

    def test_build_chart_url_fail(self):
        """test case #2 for build_equity_url_for() in reader/read.py -> throw error"""
        ticker_to_search = "invalid name..."
        with self.assertRaises(ValueError):
            reader = Reader(ticker_to_search)
            reader.build_company_lookup_url()

    def test_get_equity_chart_data_pass(self):
        """test case #1 for get_equity_chart_data() in reader/read.py -> pass"""
        reader = self.reader_co

        equity_chart_data = reader.get_equity_chart_data()

        # check some of the response data...
        self.assertEqual(list(equity_chart_data.keys()), ["chart"])
        self.assertTrue(("result" and "error") in equity_chart_data["chart"].keys())
        self.assertTrue(
            ("meta" and "timestamp" and "indicators")
            in equity_chart_data["chart"]["result"][0].keys()
        )
        self.assertIsNone(equity_chart_data["chart"]["error"])

    def test_get_equity_chart_data_fail(self):
        """test case #2 for get_equity_chart_data() in reader/read.py -> throw error"""
        ticker_to_search = "invalid name..."
        with self.assertRaises(ValueError):
            reader = Reader(ticker_to_search)

            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.build_equity_chart_url()
            reader.get_equity_chart_data()
            return reader

    def test_get_equity_quote_data_pass(self):
        """test case #1 for get_equity_quote_data() -> pass"""
        reader = self.reader_co

        equity_quote_data = reader.get_equity_quote_data()

        # check some of the response data
        self.assertEqual(list(equity_quote_data.keys()), ["quoteResponse"])
        self.assertTrue(
            ("result" and "error") in equity_quote_data["quoteResponse"].keys()
        )
        self.assertTrue(
            (
                "regularMarketPreviousClose"
                and "regularMarketPreviousOpen"
                and "regularMarketVolume"
                and "regularMarketDayLow"
                and "regularMarketDayHigh"
                and "fiftyDayAverage"
                and "bid"
                and "ask"
            )
            in equity_quote_data["quoteResponse"]["result"][0].keys()
        )
        self.assertIsNone(equity_quote_data["quoteResponse"]["error"])

    def test_get_equity_quote_data_fail(self):
        """test case #2 for get_equity_quote_data() -> throw error"""
        # ticker_to_search = "invalid name..."
        ticker_to_search = "invalid name..."
        with self.assertRaises(ValueError):
            reader = Reader(ticker_to_search)

            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.get_equity_quote_data()

    def test_private_get_pass(self):
        """test case #1 for call private method directly -> pass."""
        reader = self.reader_co

        chart_data_response = reader._get(
            Constants.yahoo_finance_base_chart_url + reader.ticker
        )

        self.assertTrue(chart_data_response["chart"]["error"] is None)
        self.assertTrue(
            ("meta" and "timestamp" and "indicators")
            in chart_data_response["chart"]["result"][0].keys()
        )

    def test_private_get_fail(self):
        """
        test case #2 for call private method directly -> fail.

        this should never happen, since a validity check is sent upon initialization to
        ensure that a ticker symbol exists in the database. But, if the private method
        were to be called directly, raise_for_status() will catch it [assuming yfinance
        responsds with a 404].
        """
        ticker_to_search = "invalid name..."

        with self.assertRaises(HTTPError):

            reader = Reader(ticker_to_search)
            reader._get(Constants.yahoo_finance_base_chart_url + ticker_to_search)

    def test_get_equity_company_data(self):
        """
        test case #1 for get_equity_company_data() -> pass.

        test the get_equity_company_data() method which uses the value passed
        upon initialization of the ``Reader`` class to ping Yahoo
        Finance's backend and render a list of possible equities.
        If no values are returned, a ``ValueError`` is thrown.
        """
        reader = self.reader_co
        company_equity_data_one = reader.get_equity_company_data(force=True)

        self.assertTrue(company_equity_data_one[0] == reader.name)
        self.assertTrue(company_equity_data_one[1] == reader.ticker)

        reader_two = self.reader_tick
        company_equity_data_two = reader_two.get_equity_company_data(force=True)

        self.assertTrue(company_equity_data_two[0] == reader_two.name)
        self.assertTrue(company_equity_data_two[1] == reader_two.ticker)

    def test_ticker_getter(self):
        """
        test case #1 for the `ticker` property.

        Expected behavior: `ticker` is implemented as a property in reader/read.py
        and has a getter and setter method. The getter method returns the value assigned
        to ticker and the setter updates/sets the value.

        This test checks to see what the value of the ticker property is post-__init__.
        """
        reader_one = self.reader_co
        reader_two = self.reader_tick

        self.assertTrue(
            reader_one.ticker != self.company_name
            if self.company_name != "AAPL"
            else reader_one.ticker == self.company_name
        )

        self.assertTrue(reader_two.ticker == self.ticker_name)  # shouldn't change!

    def test_ticker_setter(self):
        """
        test case #2 for the `ticker` property.

        Expected behavior: see test case #1.

        This test checks to see if the `ticker` property is correctly
        updated post-__init__.
        """
        reader_one = self.reader_co
        reader_two = self.reader_tick

        self.assertTrue(
            reader_one.ticker == "AAPL" and reader_two.ticker == self.ticker_name
        )

        reader_one.ticker = reader_two.ticker = "TSLA"

        self.assertTrue(reader_one.ticker == reader_two.ticker)

    def test_name_getter(self):
        """
        test case #1 for the `name` property.

        Expected behavior: Similar to the `ticker` property, the "long name"
        of a stock is mapped to this property during instantiation. These two
        properties are key to the functionality of the reverse lookup. They support
        both getting & setting.
        """
        reader_one = self.reader_co
        reader_two = self.reader_tick

        self.assertTrue(
            (reader_two.name.lower() == "salesforce.com, inc.")
            & (reader_one.name.lower() == "apple inc.")
        )

    def test_name_setter(self):
        """
        test case #2 for the `name` property.

        Expected behavior: See test case #1.

        This test checks to see that the `name` property is correctly
        updated post-__init__.
        """
        reader_apple = self.reader_co
        reader_salesforce = self.reader_tick
        new_name_apple = "Apple!"
        new_name_salesforce = "Salesforce!"

        init_name_apple = reader_apple.name
        init_name_salesforce = reader_apple.name
        reader_apple.name = new_name_apple
        reader_salesforce.name = new_name_salesforce

        self.assertTrue(
            (reader_apple.name != init_name_apple)
            & (reader_apple.name == new_name_apple)
        )

        self.assertTrue(
            (reader_salesforce.name != init_name_salesforce)
            & (reader_salesforce.name == new_name_salesforce)
        )
