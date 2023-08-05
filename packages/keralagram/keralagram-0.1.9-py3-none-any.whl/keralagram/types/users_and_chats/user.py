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


class User(object):
    @classmethod
    def de_json(cls, json_str):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError(f"Expected dict or str type got {type(json_str)}")
        id = json_obj.get("id")
        is_bot = json_obj.get("is_bot")
        first_name = json_obj.get("first_name")
        last_name = json_obj.get("last_name")
        username = json_obj.get("username")
        lang_code = json_obj.get("language_code")
        can_join_groups = json_obj.get("can_join_groups")
        can_read_all_messages = json_obj.get("can_read_all_group_messages")
        supports_inline_queries = json_obj.get("supports_inline_queries")

        return cls(id, is_bot, first_name, last_name, username, lang_code, can_read_all_messages,
                   can_join_groups, supports_inline_queries)

    def __init__(self, id, is_bot, first_name, last_name, username, lang_code,
                 can_read_all_messages, can_join_groups, supports_inline_queries):
        self.id = id
        self.is_bot = is_bot,
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.lang_code = lang_code
        self.can_join_groups = can_join_groups,
        self.can_read_all_messages = can_read_all_messages
        self.supports_inline_queries = supports_inline_queries

    @classmethod
    def get_new_chat_members(cls, users):
        result = []
        for user in users:
            result.append(User.de_json(dict(user)))
        return result
