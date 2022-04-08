from account_generator_helper.utilities import str_to_timedelta
from datetime import datetime


class Message:
    def __init__(self, sender_name, message, string_time):
        self._sender_name = sender_name
        self._message = message
        self._send_time = datetime.now() - str_to_timedelta(string_time)

    @property
    def sender_name(self):
        """
        :return: Name of sender name.
        """
        return self._sender_name

    @property
    def message(self):
        """
        :return: Message content.
        """
        return self._message

    @property
    def send_time(self):
        """
        :return: Time when message sent.
        """
        return self._send_time

    def __repr__(self):
        return '<Message from={} message={} send_time={}>'.format(self._sender_name, self._message,
                                                                  self._send_time.strftime('%Y-%m-%d %H:%M:%S'))
