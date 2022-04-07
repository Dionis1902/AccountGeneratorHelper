import re
import time
from datetime import datetime
from ..utilities import random_string


class Mail:
    def __init__(self, proxy=None):
        self._mail = None
        self._proxies = {'http': proxy, 'https': proxy} if proxy else None
        self._handlers = []

    def get_mail(self):
        return self.set_mail(random_string())

    def set_mail(self, *args, **kwargs):
        pass

    def _set_mail(self, mail):
        self._mail = mail
        return self._mail

    def get_inbox(self):
        pass

    def letter_handler(self, sender_name='', sender_mail='', subject='', re_subject=''):
        def wrapper(handler):
            self._handlers.append({'handler': handler, 'from_name': sender_name, 'from_email': sender_mail,
                                   'subject': subject, 're_subject': re_subject,
                                   'time': datetime.now()})

        return wrapper

    def _letter_handler(self, _letter):
        def __is_valid(handler):
            return (not handler['from_name'] or handler['from_name'] == _letter.from_name) and \
                   (not handler['from_email'] or handler['from_email'] == _letter.from_email) and \
                   (not handler['subject'] or handler['subject'] == _letter.subject) and \
                   (not handler['re_subject'] or re.findall(handler['re_subject'], _letter.subject)) and \
                   (not handler['time'] or handler['time'] < _letter.send_time)

        for _handler in self._handlers:
            if __is_valid(_handler):
                _handler['handler'](_letter)

    def poling(self, timeout: int = 10):
        letters = []
        try:
            while True:
                for _letter in self.get_inbox():
                    if hash(_letter) not in letters:
                        letters.append(hash(_letter))
                        self._letter_handler(_letter)
                time.sleep(timeout)
        except KeyboardInterrupt:
            pass
