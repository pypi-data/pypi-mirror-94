#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from argparse import ArgumentError
import re
import dataclasses
from typing import List
import datetime

from equit_ease.parser.parse import Parser, ChartParser
from equit_ease.utils.Constants import Constants


class Displayer(Parser):
    """contains methods relating to the displayment of quote and chart data."""

    def __init__(self, equity_to_search, data):
        super().__init__(equity_to_search, data)

    def set_formatting(self, value_to_format: str or int, formatting_type: str) -> str:
        """
        apply a template of formatting to the provided value.

        :param value_to_format -> ``str``: the value that should be formatted.
        :param formatting_type -> ``str``: the type of formatting to perform.
        :return result -> ``str``: the result to return.
        """
        result = value_to_format

        # https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
        if isinstance(formatting_type, list):
            for styling in formatting_type:
                result = Constants.dispatcher[styling](result)
        else:
            result = Constants.dispatcher[formatting_type](result)

        return result


class TrendsDisplayer(Displayer):
    """"contains methods used solely for the displayment of the chart data."""

    def __init__(self, reader):
        self.chart_one_year_url = reader.chart_one_year_url
        self.chart_six_months_url = reader.chart_six_months_url
        self.chart_three_months_url = reader.chart_three_months_url
        self.chart_one_month_url = reader.chart_one_month_url
        self.chart_five_days_url = reader.chart_five_days_url
    
    @staticmethod
    def get_percentage_change(
            start_value: int or float, end_value: int or float, num_decimal_places: int
        ) -> float:
        """
        calculate the percentage change from the beginning and ending values of a series.

        :param start_value -> ``int`` or ``float``: the starting value in the series.
        :param end_value -> ``int`` or ``float``: the ending value in the series.

        :returns result -> ``float``: the percentage change.
        """
        if not (isinstance(start_value, (int, float)) and \
            isinstance(end_value, (int, float)) and \
            isinstance(num_decimal_places, int)
        ):
            raise ArgumentError(None, message="start_value and end_value must be `int` or `float` type, and num_decimal_places must be `int`.")
        else:
            if start_value == 0:
                result = 0.0
            else:
                percent_chage_formula = ((end_value - start_value) / (start_value)) * 100
                result = round(percent_chage_formula, num_decimal_places)
            return result

    async def build_historical_price_trends(self, instance_var_to_access: str) -> str:
        """
        Given a valid class instance variable, retrieve it and use it's
        value to send a GET request to yahoo finance.

        :param instance_var_to_access -> ``str``: a valid class instance variable to access.

        :returns result -> ``float``: the percentage change for a start and end value.
        """

        attr_data = getattr(self, instance_var_to_access, None)
        if (attr_data) and (re.match(r"^(https|http)", attr_data)):
            get_request_response = self._get(attr_data)
            filtered_response_data = get_request_response["chart"]["result"][0]

            daily_close_data = ChartParser.standardize(
                self._extract_data_from(
                    filtered_response_data["indicators"]["quote"][0], "close"
                )
            )
            daily_open_data = ChartParser.standardize(
                self._extract_data_from(
                    filtered_response_data["indicators"]["quote"][0], "open"
                )
            )

            time_series_initial_open = daily_open_data[0]
            time_series_final_close = daily_close_data[-1]
            return self.get_percentage_change(
                time_series_initial_open, time_series_final_close, 3
            )
        else:
            raise ValueError(
                f"Invalid Class Instance Variable. {instance_var_to_access} does not exist."
            )

    @staticmethod
    def _build_descriptive_word_for(equity_percent_change: float) -> str:
        """
        dynamically builds a descriptive word ["up" or "down"] based on the
        value of the percent change.

        If the percent change for an equity is greater than 0, the descriptive word
        is "up". If the percent change for an equity is less than 0, the descriptive
        word is "down". Lastly, if the percent change for an equity is 0, the
        descriptive word is "unchanged".

        :param self -> ``TrendsDisplayer``:
        :param equity_percent_change -> float: the percent change for an equity as calculated by
        ``self.get_percentage_change``.

        :returns result -> ``str``: the descriptive word.
        """
        result = ""

        if equity_percent_change > 0:
            result = "⬆ (up)"
        elif equity_percent_change < 0:
            result = "⬇ (down)"
        else:
            result = "-- (unchanged)"

        return result

    async def get_trends(self, *trends):
        """
        get percentage changes for each provided arg in ``trends``.
        """
        price_trends = list()
        for trend in trends:
            result = await self.build_historical_price_trends(trend)
            price_trends.append(result)
        return price_trends

    def display(self, percentage_change: float, timeframe_descriptor: str) -> None:
        """
        display trends datapoints to the console.

        :param self -> ``TrendsDisplayer``:
        :param percentage_change -> ``float``: the percentage change in the price of an equity.
        :param timeframe_descriptor -> ``str``: a descriptor of the timeframe which is appended to the
                                                end of the base_sentence.

        :returns ``None``: rather than returning, prints to the console.
        """
        descriptive_word = self._build_descriptive_word_for(percentage_change)
        print(
            f"\t{descriptive_word} {percentage_change}% in the past {timeframe_descriptor}."
        )


class QuoteDisplayer(Displayer):
    """contains methods used solely for the displayment of quote data."""

    def tabularize(self: QuoteDisplayer) -> List[str]:
        """
        str representation of the quote meta-data.

        :param self -> ``QuoteDisplayer``:
        :returns ``List[str]``:
        """
        dataclass_as_dict = dataclasses.asdict(self.data)

        row_one = []
        row_two = []
        padding_sizes = []

        for key, value in dataclass_as_dict.items():    
            if key in Constants.default_display_data:
                if key in ('next_dividend_date', 'last_earnings_date'):
                    value = ( 
                        datetime.datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
                        if value != "N/A"
                        else "N/A"
                    )

                formatted_key = self.set_formatting(key, ["split", "capitalize"])
                max_padding = (
                    len(formatted_key)
                    if len(formatted_key) > len(str(value))
                    else len(str(value))
                )
                row_one.append(formatted_key), row_two.append(value)
                padding_sizes.append(max_padding)

        def aggregate(*args):
            result = []
            for arg in args:
                for separator in arg:
                    result.append(separator)
            return result

        return aggregate(
            self._build_table(padding_sizes, rows=[row_one]),
            self._build_table(padding_sizes, rows=[row_two]),
        )

    def _build_table(self: QuoteDisplayer, padding_size: List[int], **kwargs):
        def build_column_separators(row: List[str], padding_sizes: List[str]) -> str:
            """
            build the separators that exist between each column.

            :param row -> ``List[str]``: the row to format with separators and spacing.
            :param padding_sizes -> ``List[str]``: the sizes of padding to assign to each value.
                                                   Must be in the same order as the values they should be assigned to.
            :returns result -> ``str``: the formatted row with '|' separators between each column.

            :example:

                    >>> row = [160.8, 160.81, 169.66, 170.0, '159.44 - 178.6199', 12440181, 101560188928, 'N/A']
                    >>> padding_sizes = [5, 6, 6, 5, 17, 8, 12, 3]
                    >>> build_column_separators(row, padding_sizes)

                        | 160.8 | 160.81 | 169.66 | 170.0 | 159.44 - 178.6199 | 12440181 | 101560188928 | N/A |
            """
            result = " | "
            for i, item in enumerate(row):
                stringified_item = str(item)
                padding = padding_sizes[i]
                leading_whitespace = " " * (padding - len(str(item)))
                result += leading_whitespace + stringified_item + " | "

            return result

        def build_row_separators(row: List[str]) -> str:
            """
            build the separators that exist between each row.

            :param row -> ``List[str]``: the row used to determine the length of the separator.
            :returns result -> ``str``: a string len(row) long used as the separator.

            :example:
                1.
                    >>> build_row_sepaarators(5)
                    -----
                2.
                    >>> build_row_sepaarators(10)
                    ----------
            """
            result = "-" * (len(row))
            return result

        rows = kwargs["rows"]

        for row in rows:
            formatted_row = build_column_separators(row, padding_size)
            formatted_col = build_row_separators(formatted_row)
            return formatted_col, formatted_row