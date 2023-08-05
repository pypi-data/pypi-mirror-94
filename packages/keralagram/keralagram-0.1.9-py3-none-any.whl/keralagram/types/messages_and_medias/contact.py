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


class Contact(object):
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
        phone_number = json_obj.get("phone_number")
        first_name = json_obj.get("first_name")
        last_name = json_obj.get("last_name")
        user_id = json_obj.get("user_id")
        vcard = json_obj.get("vcard")
        return cls(phone_number, first_name, last_name, user_id, vcard)

    def __init__(self, phone_number, first_name, last_name, user_id, vcard):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard
