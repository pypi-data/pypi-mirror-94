import unittest
import argparse
import asyncio

from equit_ease.displayer.display import TrendsDisplayer
from equit_ease.reader.read import Reader

class TestTrendsDisplayer(unittest.TestCase):
    """Testing methods from the TrendsDisplayer class."""

    def setUp(self):
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
        self.ticker_name = "AAPL"
        reader_co = set_up_reader_co(Reader(self.company_name))
        reader_tick = set_up_reader_tick(Reader(self.ticker_name))

        self.trends_displayer_co = TrendsDisplayer(
            reader_co
        )
        self.trends_displayer_tick = TrendsDisplayer(
            reader_tick
        )

    def tearDown(self):
        self.trends_displayer = TrendsDisplayer
    
    def test_get_percentage_change_for_company_name(self):
        """
        Test Case #1 for get_percentage_change() -> pass.

        test that the correct percent change is returned from
        the function when ``Reader`` is instantiated with the 
        company name.
        """
        percent_change_pos_co = self.trends_displayer_co.get_percentage_change(
            start_value=75,
            end_value=200,
            num_decimal_places=2
        )


        percent_change_negative_co = self.trends_displayer_co.get_percentage_change(
            start_value=200,
            end_value=75,
            num_decimal_places=2
        )


        self.assertGreaterEqual(
            percent_change_pos_co,
            0
        )
        self.assertLessEqual(
            percent_change_negative_co,
            0
        )
    
    def test_get_percentage_change_for_ticker(self):
        """
        Test Case #2 for get_percentage_change() -> pass.

        test that the correct percent change is returned from
        the function when ``Reader`` is instantiated with ticker
        symbol.
        """
        percent_change_pos_tick = self.trends_displayer_tick.get_percentage_change(
            start_value=75,
            end_value=200,
            num_decimal_places=2
        )

        percent_change_negative_tick = self.trends_displayer_tick.get_percentage_change(
            start_value=200,
            end_value=75,
            num_decimal_places=2
        )
        
        self.assertGreaterEqual(
            percent_change_pos_tick,
            0
        )
        self.assertLessEqual(
            percent_change_negative_tick,
            0
        )
    
    def test_get_percentage_change_fail(self):
        """
        Test Case #3 for get_percentage_change() -> fail.

        test that the correct error is raised when invalid
        data is passed to get_percentage_change().

        Here, we test that the correct error is raised when a
        string is passed to `start_value` or `end_value` or a
        string or float is passed to num_decimal_places.
        """
        with self.assertRaises(argparse.ArgumentError):
            self.trends_displayer_tick.get_percentage_change(
                start_value="I am an invalid start value!",
                end_value=75,
                num_decimal_places=2
            )

        with self.assertRaises(argparse.ArgumentError):
            self.trends_displayer_tick.get_percentage_change(
                start_value=200,
                end_value="I am an invalid end value!",
                num_decimal_places=2
            )
        
        with self.assertRaises(argparse.ArgumentError):
            self.trends_displayer_tick.get_percentage_change(
                start_value=200,
                end_value=75,
                num_decimal_places=2.0
            )

        with self.assertRaises(argparse.ArgumentError):
            self.trends_displayer_tick.get_percentage_change(
                start_value=200,
                end_value=75,
                num_decimal_places="Another invalid decimal place!"
            )
    def test_build_historical_price_trends(self):
        """
        test case #1 for build_historical_price_trends() and get_trends() -> pass.

        test that the correct data type is returned from build_historical_price_trends()
        for each class instance variable.

        Since both get_trends() and build_historical_price_trends() work in tandom with
        one another, we can test them together.
        """
        class_instance_variables = self.trends_displayer_tick.__dict__.keys()
        non_private_class_instance_variables = [
            instance_var for instance_var in class_instance_variables 
            if instance_var[0] != "_"
        ]

        for instance_var in non_private_class_instance_variables:
            result = asyncio.run(self.trends_displayer_tick.build_historical_price_trends(instance_var))
            self.assertIsInstance(
                result,
                (int, float)
            )
            self.assertEqual(
                result,
                asyncio.run(self.trends_displayer_tick.get_trends(instance_var))[0]
            )