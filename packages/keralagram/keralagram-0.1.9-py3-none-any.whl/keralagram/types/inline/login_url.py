import json


class LoginUrl(object):
    def __init__(self, url, forward_text=None, bot_username=None, request_write_access=None):
        self.url = url
        self.forward_text = forward_text
        self.bot_username = bot_username
        self.request_write_access = request_write_access

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
        url = json_obj['url']
        forward_text = json_obj.get('forward_text')
        bot_username = json_obj.get('bot_username')
        request_write_access = json_obj.get('request_write_access')
        return cls(url, forward_text, bot_username, request_write_access)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'url': self.url}
        if self.forward_text:
            json_dict['forward_text'] = self.forward_text
        if self.bot_username:
            json_dict['bot_username'] = self.bot_username
        if self.request_write_access is not None:
            json_dict['request_write_access'] = self.request_write_access
        return json_dict
