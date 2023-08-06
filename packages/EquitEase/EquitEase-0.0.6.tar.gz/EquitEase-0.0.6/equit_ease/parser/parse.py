#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import dataclasses
from typing import Dict, Any, List, Tuple
import re

from equit_ease.reader.read import Reader
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants


class Parser(Reader):
    """contains parsing-related methods that are utilized by children classes."""

    def __init__(self, equity, data):
        super().__init__(equity)
        self.data = data

    def _build_dict_repr(
        self, keys_to_extract: List[str], data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        build dictionary representation with the keys to extract and the
        overarching  JSON data structure to extract from.

        :param keys_to_extract -> ``List[str]``: keys to extract.
        :param data -> ``Dict[str, Any``: the data structure to extract from.

        :returns result -> ``Dict[str, Any]``: compiled dictionary containing the keys and their extracted values.
        """
        finalized_data_struct = {}

        for key in list(keys_to_extract):
            finalized_data_struct[key] = self._extract_data_from(data, key)

        return finalized_data_struct


class QuoteParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Quote data."""

    def extract_equity_meta_data(self: QuoteParser) -> Dict[str, Any]:
        """
        extracts meta-data from the GET /quote API call. This meta-data will
        then be used to display a tabular representation of the data in the
        console.

        :params self -> ``Parser``:
        :returns -> ``EquityMeta``: dataclass defined in datatypes/equity_meta.py
        """
        equity_metadata = self.data

        y_finance_column_mappings = Constants.yahoo_finance_column_mappings
        keys_to_extract = Constants.yahoo_finance_quote_keys
        json_data_for_extraction = equity_metadata["quoteResponse"]["result"][0]

        equity_meta_data_struct = self._build_dict_repr(
            keys_to_extract, json_data_for_extraction
        )

        return self._init_dataclass(y_finance_column_mappings, equity_meta_data_struct)

    def _init_dataclass(
        self, column_mappings: List[str], finalized_data_struct: Dict[str, Any]
    ) -> EquityMeta:
        """
        initializes EquityMeta dataclass and returns it.

        :param self -> ``QuoteParser``:
        :param finalized_data_struct -> ``Dict[str, Any]``: the finalized data structure built from _build_dict_repr

        :returns result -> ``EquityMeta``: EquityMeta dataclass.
        """
        dataclass_fields = dataclasses.fields(EquityMeta)
        dataclass_kw_arg_names = [field.name for field in dataclass_fields]
        dataclass_kw_arg_vals = [
            finalized_data_struct[column_mappings[key]]
            for key in dataclass_kw_arg_names
        ]

        result = EquityMeta(
            **dict(zip(dataclass_kw_arg_names, dataclass_kw_arg_vals))
        )  # unpack key-value pairs into keyword args

        return result


class ChartParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Chart data."""

    #!TODO: Neither of these are necessary...

    @staticmethod
    def standardize(item_to_standardize: List[float or int or None]) -> List[float or int]:
        """
        retrieves the mean of the items in the list (after removing none types),
        then replaces none types with the mean

        :param self -> ``Parser``:
        :param item_to_standardize -> ``List[float | None]``: a list of items to standardize.

        :returns result -> ``List[float]``
        """
        # TODO: is there a better approach for 'standardization'? Is this approach dirtying the data?
        remove_none_types = [item for item in item_to_standardize if item is not None]

        avg_of_filtered_items = sum(remove_none_types) / len(remove_none_types)

        result = [
            item if item is not None else avg_of_filtered_items
            for item in item_to_standardize
        ]

        return result

    def extract_equity_chart_data(self: ChartParser) -> Dict[str, Any]:
        """
        extracts chart-related data from GET /chart API call. This chart data
        is then used to build a graphical representation of the stock price and/or
        volume (x-axis is time, y-axis is price | volume)
        """
        equity_chart_data = self.data["chart"]["result"][0]

        json_data_for_extraction = equity_chart_data["indicators"]["quote"][0]

        keys_to_extract = json_data_for_extraction.keys()

        equity_chart_data_struct = self._build_dict_repr(
            keys_to_extract, json_data_for_extraction
        )

        return (
            self.standardize(self._extract_data_from(equity_chart_data_struct, "low")),
            self.standardize(
                self._extract_data_from(equity_chart_data_struct, "high")
            ),
            self.standardize(
                self._extract_data_from(equity_chart_data_struct, "open")
            ),
            self.standardize(
                self._extract_data_from(equity_chart_data_struct, "close")
            ),
            self.standardize(
                self._extract_data_from(equity_chart_data_struct, "volume")
            ),
            self._extract_data_from(
                equity_chart_data, "timestamp"
            ),  # extract from base equity chart data
        )


class UserConfigParser(Reader):
    def __init__(self, list_name: str, list_of_file_contents: List[str], equities: List[str]= None) -> None:
        self.list_name = list_name
        self.list_of_file_contents = list_of_file_contents
        self.equities = equities
    
    @property
    def equities(self: UserConfigParser) -> List[str]:
        """`GETTER` for getting the equities assigned to a user-configured list."""
        return self._equities
    
    @equities.setter
    def equities(self: UserConfigParser, equities) -> None:
        """`SETTER` for setting the equities assigned to a user-configured list."""
        self._equities = equities
    
    @property
    def list_name(self: UserConfigParser) -> str:
        """`GETTER` for getting the name of the selected list."""
        return self._list_name
    
    @list_name.setter
    def list_name(self: UserConfigParser, list_name: str) -> None:
        """`SETTER` for setting the name of the selected list."""
        self._list_name = list_name


    def format_equity_lists(self: UserConfigParser) -> Tuple[list, str]:
        """
        search the lists file located in $HOME/.equit_ease/lists, gather a data
        struct of all stock list names, and format these names.

        :self -> ``UserConfigParser``:
        """
        all_list_names = filter(
            re.compile(r"^\[[a-zA-Z0-9]").search, self.list_of_file_contents
        )
        formatted_list_names = lambda list_names: [
            name.strip("[]") for name in list_names
        ]
        list_of_formatted_list_names = formatted_list_names(list(all_list_names))
        string_of_formatted_list_names = ", ".join(list_of_formatted_list_names)
        return (list_of_formatted_list_names, string_of_formatted_list_names)

    def find_match(self: UserConfigParser) -> None:
        """
        iterate over equity list names and search for a match. Then, if a match is found,
        retrieve the equities associated with that list and retrieve data for them.

        :param self -> ``UserConfigParser``:
        :returns result -> ``List[str]``: a list of the equities associated with `self.list_name`
        """
        is_match = lambda line: re.search(rf"^\[{self.list_name}\]", line)

        for i, line in enumerate(self.list_of_file_contents):
            if is_match(line):
                equity_names_to_search_unformatted = self.list_of_file_contents[i + 1]
                equity_names_to_search_formatted = (
                    equity_names_to_search_unformatted.split(" = ")[-1]
                )
                split_names = lambda name: name.split(",")
                result = split_names(equity_names_to_search_formatted)
                return result

            else:
                # otherwise, continue to next line
                continue
