#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from equit_ease.utils.Colors import Colors


class Formatter:
    """defines methods related to the formatting of string or integer data."""

    @staticmethod
    def bold(a_value: str or int) -> str:
        """
        bold a string or integer data type.
        :param a_value: ``str`` or ``int``: the value to bold.
        :return -> ``str`` or ``int``: the bolded value.
        """
        return Colors.BOLD + str(a_value) + Colors.END

    @staticmethod
    def set_color_for(a_value: str or int) -> str or int:
        """
        set the color of a string or integer.

        :param a_value -> ``str`` or ``int``: the value to 'colorize'.
        :returns result -> ``str`` or ``int``: the 'colorized' value
        """
        strinigified_value = str(a_value)

        if isinstance(a_value, (int, float)):
            if a_value >= 0:
                return Colors.GREEN + strinigified_value + Colors.END
            else:
                return Colors.RED + strinigified_value + Colors.END
        else:
            return Colors.GREEN + strinigified_value + Colors.END

    @staticmethod
    def set_size_for():
        return

    @staticmethod
    def underline(a_value):
        return Colors.UNDERLINE + str(a_value) + Colors.END

    @staticmethod
    def align(string_to_center: str) -> str:
        """
        returns a center-aligned string to the console.

        :param string_to_center -> ``str``: the string to print to the console.
        :returns result -> ``str``:
        """
        result = "{:>12}".format(string_to_center)
        return result

    @staticmethod
    def split_at(value: str) -> str:
        """
        split the value at the provided delimiter.

        :param value -> ``str``: the value to split.
        :param delimiter -> ``str``: the delimiter to split the value on.

        :returns result -> ``str``: the split value joined on " ".
        """
        result = " ".join(value.split("_"))
        return result

    def to_upper(string_to_capitalize: str) -> str:
        """
        capitalize each word in the string.

        :param string_to_capitalize -> ``str``: the string to capitalize each word.
        :return result -> ``str``: the capitalized string.
        """
        upper_case = lambda word: word.capitalize()

        split_string = string_to_capitalize.split(" ")
        if len(split_string) == 1:
            result = upper_case(string_to_capitalize)
        else:
            capitalized_words = []
            [capitalized_words.append(upper_case(word)) for word in split_string]
            result = " ".join(capitalized_words)
        return result
