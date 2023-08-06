import sys
from typing import Callable

def verify(func: Callable):
    """
    verifies whether the response from a function is not None.
    If it is None, sys.exit() is run to kill the process.

    :param func -> ``Callable``: the function whose response to verify.
    :returns ``Callable``: the 'wrapped' function.
    """
    def wrapper(*args):
        function_response = func(*args)
        if not function_response:
            sys.exit(1)
        else:
            return function_response
    return wrapper