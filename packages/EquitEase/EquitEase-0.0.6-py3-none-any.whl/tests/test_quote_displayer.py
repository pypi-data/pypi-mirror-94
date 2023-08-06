import unittest
import dataclasses
from typing import Dict
import datetime

from equit_ease.displayer.display import QuoteDisplayer
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants


def remove_unused_keys_from(dict_of_metadata: Dict[str, str]):
    """utility func used to remove unused keys from the metadata dictionary."""
    result = dict()
    for key, value in dict_of_metadata.items():
        if key in Constants.default_display_data:
            result[key] = value
        else:
            pass

    return result


class TestQuoteDisplayer(unittest.TestCase):
    """Testing methods from the Quote Displayer class."""

    def setUp(self):
        self.equity = "CRM"
        self.equity_meta = EquityMeta(
            price=225.56,
            intra_day_range="223.02 - 228.79",
            close=226.5,
            open=224.66,
            fifty_two_wk_range="115.29 - 284.5",
            market_volume=5850083,
            market_three_month_volume=9528519,
            market_ten_day_volume=7678050,
            market_cap=207004090368,
            trailing_pe=58.465527,
            forward_pe=64.44572,
            trailing_eps=3.858,
            last_earnings_date=1606838761,
            dividend_rate="N/A",
            dividend_yield="N/A",
            next_dividend_date="N/A",
        )

        self.quote_displayer = QuoteDisplayer(self.equity, self.equity_meta)

    def tearDown(self):
        self.equity = None
        self.equity_meta = EquityMeta
        self.quote_displayer = None

    def test_tabularize_data_type(self):
        """
        test case #1 for tabularize() -> pass.

        test that the type returned from tabularize() is a list containing strings.

        First, we test that the value returned is of type ``list``. Then, we loop
        through the list and check that the type of each value is of type ``str``
        """
        tabularized_metadata = self.quote_displayer.tabularize()

        self.assertIsInstance(tabularized_metadata, list)

        for item in tabularized_metadata:
            self.assertIsInstance(item, str)

    def test_tabularize_separators(self):
        """
        test case #2 for tabularize() -> pass.

        test that the separators in the table are equal in contents and
        length.

        First, we check that the separators are equal in contents with self.assertEqual.
        Then, we check that the length of the separators is 121.
        """
        tabularized_metadata = self.quote_displayer.tabularize()

        self.assertEqual(tabularized_metadata[0], tabularized_metadata[-2])

        self.assertEqual(len(tabularized_metadata[0]), 121)

    def test_tabularize_metadata(self):
        """
        test case #3 for tabularize() -> pass.

        test that the data returned at indices 1 and 3 from tabularize() matches that
        in ``self.equity_meta``.

        First, we gather some of the high-level data about the dataclass (such as field
        names and a dictionary repr. of ``self.equity_meta``). Then, we loop over the filtered
        dataclass field names and check that the values are equal to those in ``standardized_list_of_metadata``.
        """

        dataclass_fields_dict = dataclasses.asdict(self.equity_meta)
        filtered_dataclass_fields_dict = remove_unused_keys_from(dataclass_fields_dict)

        standardize = lambda list_of_items: [
            item.strip() for item in list_of_items if item.strip() != ""
        ]

        tabularized_metadata = self.quote_displayer.tabularize()

        standardized_list_of_metadata = standardize(tabularized_metadata[3].split("|"))
        filtered_dataclass_field_names = list(filtered_dataclass_fields_dict.keys())

        for i, field in enumerate(filtered_dataclass_field_names):
            if field not in ("last_earnings_date", "next_earnings_date"):
                self.assertEqual(
                    str(filtered_dataclass_fields_dict.get(field)),
                    standardized_list_of_metadata[i],
                )
            else:
                unix_time = str(filtered_dataclass_fields_dict.get(field))
                date_time = datetime.datetime.utcfromtimestamp(int(unix_time)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                self.assertEqual(date_time, standardized_list_of_metadata[i])