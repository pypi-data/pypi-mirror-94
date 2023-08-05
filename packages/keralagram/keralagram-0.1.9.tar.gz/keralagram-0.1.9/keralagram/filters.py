import re
from typing import Union


class Filters(object):
    def __init__(self):
        self.commands = {}

    @staticmethod
    def command(string, prefixes: Union[list, str] = None):
        if not isinstance(string, str):
            raise TypeError(f"Expected string type got {type(string).__name__}")

        if type(prefixes) is list:
            for li in prefixes:
                if string.startswith(li) and re.search(f"^{li}{string[1:]} .*", string):
                    return True, string[1:]
                else:
                    return False, string
