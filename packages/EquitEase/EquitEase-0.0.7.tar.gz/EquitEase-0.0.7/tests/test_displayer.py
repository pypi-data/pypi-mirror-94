import unittest

from equit_ease.displayer.display import Displayer
from equit_ease.datatypes.equity_meta import EquityMeta


class TestDisplayer(unittest.TestCase):
    """Testing methods from the Displayer class."""

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

        self.displayer = Displayer(self.equity, self.equity_meta)

    def tearDown(self):
        self.equity = None
        self.equity_meta = EquityMeta
        self.displayer = None
    
    def test_set_formatting(self):
        """
        test case #1 for ``set_formatting`` -> pass.

        this tests that the correct styling templates are provided
        to the value pass to ``set_formatting``.
        """
        self.assertEqual(
            self.displayer.set_formatting("intra_day_range", ["split", "capitalize"]),
            "Intra Day Range"
        )

        self.assertEqual(
            self.displayer.set_formatting("intra day range", ["split", "capitalize"]),
            "Intra Day Range"
        )

    def test_set_formatting_errant(self):
        """
        test case #2 for ``set_formatting`` -> fail.

        this tests that a KeyError is raised when an invalid
        formatting type is passed to ``set_formatting()``.
        """
        with self.assertRaises(KeyError):
            self.displayer.set_formatting("intra day range", ["invalid key name"])