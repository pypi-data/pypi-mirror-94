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

from aiohttp import ClientSession

from ._settings import Command, CommandChoice
from ._exceptions import (
    SlashCordException,
    HttpException,
    CommandConfigException,
    InvalidName,
    InvalidDescription,
    InvalidChoiceName
)
from ._http import HttpClient

assert Command
assert CommandChoice

assert SlashCordException
assert HttpException
assert CommandConfigException
assert InvalidName
assert InvalidDescription
assert InvalidChoiceName


__version__ = "0.0.1"
__url__ = "https://slashcord.readthedocs.io/en/latest/"
__description__ = "Discord's slash commands built for asyncio python."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "MIT"


class SlashCord(HttpClient):
    BASE_URL = "https://discord.com/api/v8/"

    def __init__(self, token: str, client_id: int,
                 public_key: str) -> None:
        if len(token) == 32:
            auth = "Bearer "
        else:
            auth = "Bot "

        auth += token

        self._requests = ClientSession(
            headers={"Authorization": auth}
        )

        self._client_id = client_id
        self._public_key = public_key

    async def close(self) -> None:
        """Close underlying sessions.
        """

        await self._requests.close()

    async def create_command(self, command: Command) -> None:
        data = await self._post(
            "/applications/{}/commands".format(self._client_id),
            payload=command._payload
        )

        print(data)
