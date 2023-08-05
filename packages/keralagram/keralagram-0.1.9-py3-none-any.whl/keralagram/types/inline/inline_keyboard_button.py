import json
from .login_url import LoginUrl


class InlineKeyboardButton(object):
    def __init__(self, text, url: str = None, callback_data: str = None, switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None, callback_game: str = None, pay: str = None,
                 login_url: LoginUrl = None):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay
        self.login_url = login_url

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
        text = json_obj['text']
        url = json_obj.get('url')
        callback_data = json_obj.get('callback_data')
        switch_inline_query = json_obj.get('switch_inline_query')
        switch_inline_query_current_chat = json_obj.get('switch_inline_query_current_chat')
        callback_game = json_obj.get('callback_game')
        pay = json_obj.get('pay')
        login_url = LoginUrl.de_json(json_obj.get('login_url'))
        return cls(text, url, callback_data, switch_inline_query, switch_inline_query_current_chat, callback_game, pay,
                   login_url)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'text': self.text}
        if self.url:
            json_dict['url'] = self.url
        if self.callback_data:
            json_dict['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            json_dict['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            json_dict['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            json_dict['callback_game'] = self.callback_game
        if self.pay is not None:
            json_dict['pay'] = self.pay
        if self.login_url is not None:
            json_dict['login_url'] = self.login_url.to_dict()
        return json_dict
