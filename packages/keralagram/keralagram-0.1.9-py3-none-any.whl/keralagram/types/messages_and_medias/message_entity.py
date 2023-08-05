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

import json
from ..users_and_chats.user import User


class MessageEntity(object):

    @classmethod
    def de_json(cls, json_str: dict):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")

        type = json_obj.get("type")
        offset = json_obj.get("offset")
        length = json_obj.get("length")
        url = json_obj.get("url")
        if json_obj.get("user") is not None:
            user = User.de_json(dict(json_obj.get("user")))
        else:
            user = None
        language = json_obj.get("language")

        return cls(type, offset, length, url, user, language)

    def __init__(self, type, offset, length, url, user, language):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

    @classmethod
    def parse_entities(cls, message_entity):
        result = []
        for me in message_entity:
            result.append(MessageEntity.de_json(dict(me)))
        return result
