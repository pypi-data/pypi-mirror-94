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


class Location(object):
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

        longitude = json_obj.get("longitude")
        latitude = json_obj.get("latitude")
        horizontal_accuracy = json_obj.get("horizontal_accuracy")
        live_period = json_obj.get("live_period")
        heading = json_obj.get("heading")
        proximity_alert_radius = json_obj.get("proximity_alert_radius")

        return cls(longitude, latitude, horizontal_accuracy, live_period, heading,
                   proximity_alert_radius)

    def __init__(self, longitude, latitude, horizontal_accuracy, live_period, heading,
                 proximity_alert_radius):
        self.longitude = longitude
        self.latitude = latitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius
