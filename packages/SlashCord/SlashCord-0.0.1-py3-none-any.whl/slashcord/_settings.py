"""MIT License

Copyright (c) 2021 Slashcord

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import re
from typing import Any, List, Optional

from ._exceptions import (
    InvalidName,
    InvalidDescription,
    InvalidChoiceName
)


# Types
SUB_COMMAND = 1
SUB_COMMAND_GROUP = 2
STRING = 3
INTEGER = 4
BOOLEAN = 5
USER = 6
CHANNEL = 7
ROLE = 8

# Regexps
ROOT_NAME_REGEX = r"^[\w-]{3,32}$"
NAME_REGEX = r"^[\w-]{1,32}$"


def check_length(value: str, exception: Exception,
                 min_: int = 1, max_: int = 100) -> None:
    """Used to check length of value and raise exception
       if not matched.

    Parameters
    ----------
    value : str
    exception : Exception
    min_ : int, optional
        by default 1
    max_ : int, optional
        by default 100

    Raises
    ------
    exception
        Whatever expection was passed.
    """

    value_len = len(value)
    if value_len < min_ or value_len > max_:
        raise exception()


class CommandChoice:
    def __init__(self, name: str, value: str) -> None:
        check_length(name, InvalidChoiceName)

        self._name = name
        self._value = value


class CommandType:
    def __init__(self, upper: Command, option: List[Any]) -> None:
        self._upper = upper
        self._option = option

    def string(self, choices: Optional[List[CommandChoice]] = None
               ) -> Command:

        self._option["type"] = STRING

        if choices:
            self._option["choices"] = [{
                "name": choice._name,
                "value": choice._value
            } for choice in choices]

        return self._upper


class Command:
    def __init__(self, name: str, description: str) -> None:
        """Used to configure a command.

        Parameters
        ----------
        name : str
            Name of command, e.g. 'blep'
        description : str
            Description of command, e.g. 'Send a random adorable animal photo'

        Raises
        ------
        InvalidName
        InvalidDescription
        """

        if not re.search(ROOT_NAME_REGEX, name):
            raise InvalidName()

        check_length(description, InvalidDescription)

        self._payload = {
            "name": name,
            "description": description,
            "options": []
        }

    def option(self, name: str, description: str,
               required: bool = False
               ) -> CommandType:

        if not re.search(NAME_REGEX, name):
            raise InvalidName()

        check_length(description, InvalidDescription)

        option = {
            "name": name,
            "description": description,
            "required": required
        }

        self._payload["options"].append(option)

        return CommandType(self, self._payload["options"][-1])
