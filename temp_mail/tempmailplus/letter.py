import requests
from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, to, mail, proxies):
        super().__init__(to, mail['from_name'], mail['from_mail'], mail['subject'], datetime.strptime(mail['time'], '%Y-%m-%d %H:%M:%S'), proxies)
        self.__letter_id = mail['mail_id']

    @property
    def letter(self):
        if self._latter:
            return self._latter
        r = requests.get(f'https://tempmail.plus/api/mails/{self.__letter_id}?email={self._email}', proxies=self._proxies)
        if r.status_code == 200:
            self._latter = r.json()['text']
            return self._latter
