import json
from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup(object):
    max_row_keys = 8

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
        keyboard = [[InlineKeyboardButton.de_json(button) for button in row] for row in json_obj['inline_keyboard']]
        return cls(keyboard)

    def __init__(self, keyboard: list[list[InlineKeyboardButton]]):
        self.keyboard = keyboard if keyboard else []

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = dict()
        json_dict['inline_keyboard'] = [[button.to_dict() for button in row] for row in self.keyboard]
        return json_dict
