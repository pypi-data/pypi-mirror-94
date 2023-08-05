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
from .poll_option import PollOption
from ..messages_and_medias .message_entity import MessageEntity


class Poll(object):
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
        id = json_obj.get("id")
        question = json_obj.get("question")
        if json_obj.get("options") is not None:
            options = PollOption.get_poll_options(json_obj.get("options"))
        else:
            options = None

        total_voter_count = json_obj.get("total_voter_count")
        is_closed = json_obj.get("is_closed")
        is_anonymous = json_obj.get("is_anonymous")
        type = json_obj.get("type")
        allows_multiple_answers = json_obj.get("allows_multiple_answers")
        correct_option_id = json_obj.get("correct_option_id")
        explanation = json_obj.get("explanation")

        if json_obj.get("explanation_entities") is not None:
            explanation_entities = MessageEntity.parse_entities(json_obj.get("explanation_entities"))
        else:
            explanation_entities = None
        open_period = json_obj.get("open_period")
        close_date = json_obj.get("close_date")

        return cls(id, question, options, total_voter_count, is_closed, is_anonymous,
                   type, allows_multiple_answers, correct_option_id, explanation, explanation_entities,
                   open_period, close_date)

    def __init__(self, id, question, options, total_voter_count, is_closed, is_anonymous,
                 type, allows_multiple_answers, correct_option_id, explanation, explanation_entities,
                 open_period, close_date):
        self.id = id
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.explanation_entities = explanation_entities
        self.open_period = open_period
        self.close_date = close_date
