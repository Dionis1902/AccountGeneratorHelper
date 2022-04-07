import time
import requests
from temp_mail.inboxkitten.letter import Letter
from temp_mail.exceptions import NotSetEmail
from temp_mail.utilities import random_string


class InboxKittenMail:
    def __init__(self, proxy=None):
        self.__mail = None
        self.__proxies = {'http': proxy, 'https': proxy} if proxy else None
        self.__handles = []

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
            letters = [Letter(__letter['storage']['url'], __letter['message']['headers'], __letter['timestamp'], self.__proxies) for __letter in r.json()]
            return letters
        return []

    def poling(self, timeout: int = 10):
        letters = []
        try:
            while True:
                for _letter in self.get_inbox():
                    if hash(_letter) not in letters:
                        letters.append(hash(_letter))
                        print(_letter)

                time.sleep(timeout)
        except KeyboardInterrupt:
            pass
