# Keralagram - Telegram Bot Api Library Python
# Copyright (C) 2021  Anandpskerala <anandpskerala@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import re

from .types import Update, Message
from .bot import KeralaGram
from typing import Union
from keralagram import __version__


class Dispatcher(object):

    def __init__(self, bot):
        if not isinstance(bot, KeralaGram):
            raise TypeError(f'Expected class KeralaGram got {type(bot).__name__}')

        self.bot = bot
        self.running = False
        self.commands = []
        self.process_loop = asyncio.get_event_loop()
        self.plugins = self.bot.plugins
        self.logger = logging.getLogger(__name__)
        self.event_loop = asyncio.get_event_loop()

    def loop(self):
        self.running = True
        while self.running:
            updates = self.bot.retrieve_updates(offset=self.bot.offset + 1)
            self.process_updates(updates)

    def run(self):
        bot = self.bot.get_bot()
        print(f"KeralaGram version : {__version__}")
        print(f'KeralaGram (Bot) started on {bot.username}')
        print(f'Copyright (C) 2021 <\.ᴀɴᴀɴᴅ./> <https://github.com/anandpskerala>')
        print(f"Licensed under the terms of the GNU Lesser General Public License v3 or later (LGPLv3+)")
        for command, handler, _ in self.commands:
            self.logger.info(f"[COMMAND] [LOADED] \'{command}\' for {handler}")
        run_up = asyncio.ensure_future(self.loop())
        try:
            self.event_loop.run_until_complete(run_up)
        except KeyboardInterrupt:
            self.stop()
            run_up.cancel()
            self.event_loop.close()

    def stop(self):
        self.running = False

    def on_command(self, command: Union[str, list], prefixes: Union[list, str] = "/"):
        def decorator(func):
            self.add_command(command, func, prefixes)

        return decorator

    def add_command(self, command, function, prefixes: Union[list, str] = "/"):
        self.commands.append((command, function, prefixes))

    def add_command_handler(self):
        pass

    def process_command_update(self, message: Message):
        for commands, handler, prefixes in self.commands:
            if message.text:
                if type(prefixes) is str:
                    if message.text.startswith(prefixes):
                        pass
                else:
                    for pre in prefixes:
                        if message.text.startswith(pre):
                            pass

                if type(commands) is str:
                    m = re.search(commands, message.text, re.I)
                    if m:
                        message.bot = self.bot
                        return self.process_loop.run_until_complete(handler(self.bot, message))
                else:
                    for command in commands:
                        m = re.search(command, message.text, re.I)
                        if m:
                            message.bot = self.bot
                            return self.process_loop.run_until_complete(handler(self.bot, message))

    def process_updates(self, updates: list[Update]):
        for update in updates:
            self.bot.offset = max(self.bot.offset, update.update_id)
            if len(self.commands) != 0:
                if update.message:
                    self.process_command_update(update.message)
