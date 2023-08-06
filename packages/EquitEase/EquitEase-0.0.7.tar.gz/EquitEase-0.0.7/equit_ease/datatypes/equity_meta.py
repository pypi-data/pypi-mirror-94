#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Tuple


@dataclass
class EquityMeta:
    """
    Intermediary data structure utilized for the transportation of Equity Quote metadata
    during the execution of the program. This data is used to display useful information
    about a stock (bid, ask, open, close, etc...) in the terminal.
    """

    price: float # current price (if market is operating)
    intra_day_range: Tuple[float, float]  # low - high price for the stock [intra-day]
    close: float  # previous days closing stock price
    open: float  # stock price at open
    fifty_two_wk_range: Tuple[
        float, float
    ]  # low - high price for the stock [last year]

    market_volume: int
    market_three_month_volume: int
    market_ten_day_volume: int
    # intra_day volume, monthly avg. volume, and ten_day avg. volume
    market_cap: int  # stock price * shares outstanding
    trailing_pe: float
    forward_pe: float
    # trailing PE is current share price / EPS over the previous 12 months ||
    # forward PE is current share price / EPS estimation over next 12 months

    trailing_eps: float  # earnings generated over previous year
    last_earnings_date: int  # unix epoch time
    dividend_rate: float  # annual amount of cash returned to shareholders as a % of a companys share price (market value)
    dividend_yield: float  # amount a company pays shareholders divided by its current stock price
    next_dividend_date: int  # unix epoch time

    # bid: float  # highest price a buyer will pay
    # ask: float  # lowest price a seller will accept

    def __post_init__(self):
        self.volume_stats = {
            "regular_volume": self.market_volume,
            "three_month_volume": self.market_three_month_volume,
            "ten_day_volume": self.market_ten_day_volume,
        }

        self.trailing_and_forward_pe = {
            "trailing_pe": self.trailing_pe,
            "forward_pe": self.forward_pe,
        }
