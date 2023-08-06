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

import logging

from aiohttp import ClientSession, ClientResponse
from json import JSONDecodeError

from ._exceptions import HttpException


class HttpClient:
    BASE_URL: str
    _requests: ClientSession

    async def __handle_resp(self, resp: ClientResponse) -> dict:
        try:
            json = await resp.json()
        except JSONDecodeError:
            raise HttpException()
        else:
            if resp.status in (200, 201):
                return json
            else:
                logging.error(json)
                raise HttpException()

    async def _post(self, pathway: str, payload: dict) -> dict:
        async with self._requests.post(self.BASE_URL + pathway,
                                       json=payload) as resp:
            await self.__handle_resp(resp)
