#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, Any
import requests

from equit_ease.utils.Constants import Constants


class Reader:
    """
    The entrypoint for any submission; This class requests and reads data from two main Yahoo Finance endpoints: `quote` and `chart`.

    There is no parsing, cleaning or structuring done in this class. It's only purpose is to validate the input, send a
    request to an endpoint, verify the responses validity, and return it.

    This implementation aims to follow the Builder design pattern, where the construction of a complex object is separated from
    its representations. In this specific use case, the data is simply requested for, but there is no parsing or re-structuring.
    That is left to the `Parser` class. This makes it easy for the `Reader` class to be reused, amongst other things.
    """

    def __init__(self, equity: str) -> None:
        # Method Resolution Order: https://stackoverflow.com/questions/42413670/whats-the-difference-between-super-and-parent-class-name
        super().__init__()
        self.equity = equity

    def _get(self, y_finance_formatted_url: str) -> Dict[str, Any]:
        """
        private method which sends the GET request to yahoo finance,
        ensures the response is accurate, and, upon validation, returns it.

        :param y_finance_formatted_url -> ``str``: formatted Yahoo Finance URL (
            see ``build_equity_url`` for what the formatted URL should look like.
        )

        :returns result -> ``Dict[str, Any]``: JSON response object from yahoo finance.
        """
        response = requests.get(y_finance_formatted_url)
        response.raise_for_status()

        result = response.json()

        return result

    @staticmethod
    def _extract_data_from(json_data: Dict[str, Any], key_to_extract: str) -> Any:
        """
        extract ``key_to_extract`` from ``json_data``

        :param json_data -> ``Dict[str, Any]``: JSON response object from any GET /<yahoo_finance_endpoint> which returns JSON data.
        :param key_to_extract -> ``str``: the key to extract from the JSON object.
        :returns result -> ``str`` || ``int``: the value extracted from the key.
        """
        if key_to_extract not in json_data.keys():
            result = "N/A"
        else:
            result = json_data[key_to_extract]
        return result

    def set_ticker_and_name_props_to(self, ticker_val: str, name_val: str) -> None:
        """
        handle setting the `ticker` and `name` props for the class
        instance. Since these two setters are called in tandom, it
        makes most sense to extrapolate them to a public method
        that is called with the values to set.

        :param reader -> ``Reader``: an instianted Reader class obj.
        :param ticker_val -> ``str``: the value to set to the ticker property.
        :param name_val -> ``str``: the value to set to the name property.
        :returns -> ``None``: Modifies the current reader object, therefore
                                no need to return it.
        """
        self.ticker = ticker_val
        self.name = name_val

    def build_urls(self):
        """
        calls private methods that build the Quote and Chart URLs.

        :parm self -> ``Reader``:
        :return -> ``None``:
        """
        self.build_equity_quote_url()
        self.build_equity_chart_url()

    def get_data(self):
        """
        public interface used to call the private methods that retrieve
        quote and chart-related datapoints.

        :param self -> ``Reader``:
        """
        equity_quote_data = self.get_equity_quote_data()

        return equity_quote_data

    @property
    def ticker(self: Reader) -> str:
        """getter for the ticker attribute."""
        return self.__ticker

    @ticker.setter
    def ticker(self: Reader, ticker_value: str) -> None:
        """setter for the ticker attribute."""
        self.__ticker = ticker_value

    @property
    def name(self: Reader) -> str:
        """getter for the name attribute."""
        return self.__name

    @name.setter
    def name(self: Reader, name_value: str) -> None:
        """setter for the name attribute."""
        self.__name = name_value

    def build_equity_chart_url(self: Reader) -> str:
        """
        Creates the equity chart URL for a given currency.
        This URL is then used for the retrieval of data-points pertaining to
        the chart.

        :param self -> ``Reader``:
        :returns True -> ``bool``:
        """
        base_chart_url = Constants.yahoo_finance_base_chart_url
        base_params = Constants.chart_url_base_params

        def build_params(**kwargs) -> str:
            """
            build params for the GET /chart URL.

            :returns result -> ``str``: the params to be appended to the URL.
            """
            result = "?"
            list_of_param_tuples = list(kwargs.items())

            for key, value in list_of_param_tuples:
                param = (
                    f"{key}={value}" + "&"
                    if key != list_of_param_tuples[-1][0]
                    else f"{key}={value}"
                )
                result += param
            return result

        def build_url(params: str) -> str:
            """
            Given a string of params for the url, builds out the url and
            returns it fully-formatted.

            :param params -> ``str``: the params for the URL.

            :returns result -> ``str``: the formatted URL.
            """
            base_domain = base_chart_url + self.__ticker
            result = base_domain + params

            return result

        one_year_params = build_params(**base_params, range="1y")
        six_month_params = build_params(**base_params, range="6mo")
        three_month_params = build_params(**base_params, range="3mo")
        one_month_params = build_params(**base_params, range="1mo")
        five_day_params = build_params(**base_params, range="5d")

        one_year_url = build_url(one_year_params)
        six_months_url = build_url(six_month_params)
        three_months_url = build_url(three_month_params)
        one_month_url = build_url(one_month_params)
        five_days_url = build_url(five_day_params)

        result = base_chart_url + self.__ticker

        self.chart_base_url = result
        self.chart_one_year_url = one_year_url
        self.chart_six_months_url = six_months_url
        self.chart_three_months_url = three_months_url
        self.chart_one_month_url = one_month_url
        self.chart_five_days_url = five_days_url
        return True

    def build_equity_quote_url(self: Reader) -> str:
        """
        Creates the quote URL for a given equity.
        This URL is then used for the retrieval of data-points pertaining to
        equity meta-data such as EPS, P/E ratio, 52 wk high and low, etc...

        :param self -> ``Reader``:
        :returns -> ``str``: the formatted URL used to retrieve equity meta-data from yahoo finance.
        """
        base_quote_url = Constants.yahoo_finance_base_quote_url
        # TODO: this could be more robust based off args that can be passed via command-line
        result = base_quote_url + f"?symbols={self.__ticker}"

        self.quote_url = result
        return True

    def build_company_lookup_url(self: Reader) -> str:
        """
        Creates the company lookup URL based on the value passed during instantiation
        of the class.

        :param self -> ``Reader``:
        :return result -> ``str``: the URL to use for self._get()
        """
        base_company_url = Constants.yahoo_finance_co_lookup

        def is_valid(equity: requests.get) -> bool:
            """
            runs a quick validity check to ensure there are quotes matching
            the passed values. If there aren't, a ``ValueError`` is raised.
            """
            """
            Runs a quick validity check for the passed Ticker.

            If error is null, True is returned. Otherwise, False is returned and an error is thrown.

            :param ticker_url -> ``str``: the URL of the ticker.
            """
            json_response = requests.get(equity).json()

            return json_response["quotes"] != []

        def build_equity_param() -> str:
            """
            local scope function for building the equity param for the GET request.

            :returns result -> ``str``: the equity param formatted for the GET request.
            """
            split_equity = self.equity.split(" ")
            result = "+".join(split_equity)

            return result

        result = base_company_url + build_equity_param()

        if is_valid(result):
            self.company_url = result
            return True
        raise ValueError("Search returned no results.")

    def get_equity_chart_data(self: Reader) -> str:
        """
        calls the _get() private method.

        :returns -> ``Dict[str, Any]``: JSON object response from Yahoo Finance
        """
        return self._get(self.chart_base_url)

    def get_equity_quote_data(self: Reader) -> str:
        """
        calls the _get() private method.

        :returns -> ``Dict[str, Any]``: JSON object response from Yahoo Finance
        """
        return self._get(self.quote_url)

    def get_equity_company_data(self: Reader, **kwargs) -> Dict[str, Any]:
        """
        the 'equity' value passed upon initialization is used to perform a
        'reverse lookup'.

        The 'equity' value is used to query a Yahoo Finance endpoint which
        returns the long name and ticker symbol (amongst other things) for
        a stock. These two attributes are set with getter/setter methods
        and the ticker symbol is then used throughout the hierarchical
        structure to query yahoo finance.

        :param self -> ``Reader``:
        :returns result -> ``Dict[str, Any]``: Dict containing short name and ticker symbol data.
        """
        json_response = self._get(self.company_url)

        def extract_longname(data):
            """extract 'longname' from JSON object."""
            return self._extract_data_from(data, "longname")

        def extract_ticker(data):
            """extract ticker symbol from JSON object."""
            return self._extract_data_from(data, "symbol")

        def extract_quotes(data):
            """extra all quotes from JSON object."""
            choices = []
            for items in data:
                choices.append(items["symbol"])
            return choices

        long_name = extract_longname(json_response["quotes"][0])
        ticker = extract_ticker(json_response["quotes"][0])

        result = [long_name, ticker]

        if kwargs["force"] == "False":
            result.append(extract_quotes(json_response["quotes"]))
        return result
