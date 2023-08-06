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

import asynctest

from . import SlashCord, Command, CommandChoice


class TestSlashCord(asynctest.TestCase):
    use_default_loop = True

    async def setUp(self) -> None:
        self.slash_cord = SlashCord(
            token="...",
            client_id="...",
            public_key="..."
        )

    async def tearDown(self) -> None:
        await self.slash_cord.close()

    async def test_create_command(self) -> None:
        await self.slash_cord.create_command(
            Command(
                "hello", "Command created by SlashCord for testing"
            ).option(
                "choice", "Choices you can select", required=True
            ).string([
                CommandChoice("Choice 1", "choice_1")
            ])
        )
