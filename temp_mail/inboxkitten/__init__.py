import re
from datetime import datetime
import time
import requests
from temp_mail.inboxkitten.letter import Letter
from temp_mail.exceptions import NotSetEmail
from temp_mail.utilities import random_string


class InboxKittenMail:
    def __init__(self, proxy=None):
        self.__mail = None
        self.__proxies = {'http': proxy, 'https': proxy} if proxy else None
        self.__handlers = []

    def get_mail(self):
        self.set_mail(random_string())
        return self.__mail

    def set_mail(self, mail):
        self.__mail = mail

    def get_inbox(self) -> list[Letter]:
        if not self.__mail:
            raise NotSetEmail()

        r = requests.get(f'https://inboxkitten.com/api/v1/mail/list?recipient={self.__mail}', proxies=self.__proxies)
        if r.status_code == 200:
            letters = [Letter(__letter['storage']['url'], __letter['message']['headers'], __letter['timestamp'],
                              self.__proxies) for __letter in r.json()]
            return letters
        return []

    def letter_handler(self, sender_name='', sender_mail='', subject='', re_subject='', only_new: bool = True):
        def wrapper(handler):
            self.__handlers.append({'handler': handler, 'sender_name': sender_name, 'sender_mail': sender_mail,
                                    'subject': subject, 're_subject': re_subject,
                                    'time': datetime.now() if only_new else None})

        return wrapper

    def __letter_handler(self, _letter):
        for handler in self.__handlers:
            if (not handler['sender_name'] or handler['sender_name'] == _letter.sender_name) and \
                    (not handler['sender_mail'] or handler['sender_mail'] == _letter.sender_mail) and \
                    (not handler['subject'] or handler['subject'] == _letter.subject) and \
                    (not handler['re_subject'] or re.findall(handler['re_subject'], _letter.subject)) and \
                    (not handler['time'] or handler['time'] < _letter.send_time):
                handler['handler'](_letter)

    def poling(self, timeout: int = 10):
        letters = []
        try:
            while True:
                for _letter in self.get_inbox():
                    if hash(_letter) not in letters:
                        letters.append(hash(_letter))
                        self.__letter_handler(_letter)
                time.sleep(timeout)
        except KeyboardInterrupt:
            pass
