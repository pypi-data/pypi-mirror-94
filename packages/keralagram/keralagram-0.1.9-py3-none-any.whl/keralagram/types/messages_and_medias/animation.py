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
from .photo_size import PhotoSize


class Animation(object):
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

        file_id = json_obj.get("file_id")
        file_unique_id = json_obj.get("file_unique_id")
        width = json_obj.get("width")
        height = json_obj.get("height")
        duration = json_obj.get("duration")
        if json_obj.get("thumb") is not None:
            thumb = PhotoSize.de_json(dict(json_obj.get("thumb")))
        else:
            thumb = None
        file_name = json_obj.get("file_name")
        mime_type = json_obj.get("mime_type")
        file_size = json_obj.get("file_size")

        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name,
                   mime_type, file_size)

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name,
                 mime_type, file_size):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
