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
from ..messages_and_medias.pinnedmessage import PinnedMessage


class Chat(object):
    @classmethod
    def de_json(cls, json_str):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")

        id = json_obj.get("id")
        type = json_obj.get("type")
        title = json_obj.get("title")
        username = json_obj.get("username")
        first_name = json_obj.get("first_name")
        last_name = json_obj.get("last_name")
        bio = json_obj.get("bio")
        description = json_obj.get("description")
        if json_obj.get("pinned_message") is not None:
            pinned_message = PinnedMessage.de_json(dict(json_obj['pinned_message']))
        else:
            pinned_message = None
        if username is not None:
            invite_link = f"https://t.me/{json_obj.get('invite_link')}"
        else:
            invite_link = json_obj.get("invite_link")
        slow_mode_delay = json_obj.get("slow_mode_delay")
        sticker_set_name = json_obj.get("sticker_set_name")
        can_set_sticker_set = json_obj.get("can_set_sticker_set")
        linked_chat_id = json_obj.get("linked_chat_id")

        return cls(id, type, title, username, first_name, last_name, bio, description, pinned_message,
                   invite_link, slow_mode_delay, sticker_set_name, can_set_sticker_set, linked_chat_id)

    def __init__(self, id, type, title, username, first_name, last_name, bio, description, pinned_message,
                 invite_link, slow_mode_delay, sticker_set_name, can_set_sticker_set, linked_chat_id):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.description = description
        self.pinned_message = pinned_message
        self.invite_link = invite_link
        self.slow_mode_delay = slow_mode_delay
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.linked_chat_id = linked_chat_id
