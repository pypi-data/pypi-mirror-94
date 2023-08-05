import os
import sys

from .notifiers import SlackNotifier


class Notifier:
    def __init__(self, service, debug=False):
        if not service:
            raise ValueError("Parameter service must be not empty")
        if not isinstance(service, str):
            raise TypeError("Parameter service must be str")
        self.service = service
        self.debug = debug

    def get_object(self, **kwargs):
        if self.service == 'slack':
            return SlackNotifier(kwargs.get('slack_url'), kwargs.get('slack_channel'), kwargs.get('slack_username'),
                                 self.debug)


class Utils:
    @staticmethod
    def get_error_data():
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return file_name, exc_tb.tb_lineno, exc_type
