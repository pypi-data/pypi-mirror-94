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


class PinnedMessage(object):
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
        message_id = json_obj.get("message_id")
        date = json_obj.get("date")
        text = json_obj.get("text")
        forward_from_message_id = json_obj.get("forward_from_message_id")
        forward_signature = json_obj.get("forward_signature")
        forward_sender_name = json_obj.get("forward_sender_name")
        forward_date = json_obj.get("forward_date")
        edit_date = json_obj.get("edit_date")
        media_group_id = json_obj.get("media_group_id")
        author_signature = json_obj.get("author_signature")
        caption = json_obj.get("caption")
        if json_obj.get("from") is not None:
            from_user = User.de_json(dict(json_obj["from"]))
        else:
            from_user = None

        if json_obj.get("forward_from") is not None:
            forward_from = User.de_json(dict(json_obj["forward_from"]))
        else:
            forward_from = None

        if json_obj.get("via_bot") is not None:
            via_bot = User.de_json(dict(json_obj["via_bot"]))
        else:
            via_bot = None

        return cls(message_id, date, text, forward_from_message_id, forward_signature,
                   forward_sender_name, forward_date, edit_date, media_group_id, author_signature,
                   caption, from_user, forward_from, via_bot)

    def __init__(self, message_id, date, text, forward_from_message_id, forward_signature,
                 forward_sender_name, forward_date, edit_date, media_group_id, author_signature,
                 caption, from_user, forward_from, via_bot):
        self.message_id = message_id
        self.date = date
        self.text = text
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_sender_name = forward_sender_name
        self.forward_date = forward_date
        self.forward_from = forward_from
        self.from_user = from_user
        self.edit_date = edit_date
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.caption = caption
        self.via_bot = via_bot