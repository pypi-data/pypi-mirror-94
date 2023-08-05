import json
import requests


class SlackNotifier:
    LEVELS = (
        ("DEBUG", 10),
        ("INFO", 20),
        ("WARNING", 30),
        ("ERROR", 40),
        ("CRITICAL", 50),
    )

    def __init__(self, slack_url: str, slack_channel: str, slack_username: str, debug: bool):
        if not isinstance(slack_url, str):
            raise TypeError("parameter slack_url must be str")
        if not isinstance(slack_channel, str):
            raise TypeError("parameter slack_channel must be str")
        if not isinstance(slack_username, str):
            raise TypeError("parameter slack_username must be str")
        self.slack_url = slack_url
        self.slack_channel = slack_channel
        self.slack_username = slack_username
        self.debug = debug

    def push_notification(self, level, message: dict):
        if not self.debug:
            requests.post(self.slack_url, data=json.dumps({
                "channel": self.slack_channel,
                "username": self.slack_username,
                "text": self.get_message(level, message)
            }))

    def get_message(self, level, message) -> str:
        if not isinstance(message, dict) and not isinstance(message, str):
            raise TypeError("parameter message must be dict or string")
        if isinstance(message, str):
            message = {"Message": message}

        text = f'*Level: {self.get_level(level)[0]}* \n'
        text += ''.join([f'*{key}:* {value} \n' for key, value in message.items()])

        return text

    def get_level(self, level):
        for value in self.LEVELS:
            if level in value:
                return value

    def debug(self, message):
        self.push_notification(10, message)

    def info(self, message):
        self.push_notification(20, message)

    def warning(self, message):
        self.push_notification(30, message)

    def error(self, message):
        self.push_notification(40, message)

    def critical(self, message):
        self.push_notification(50, message)
