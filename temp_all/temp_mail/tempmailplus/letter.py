import requests
from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, to, mail, proxies):
        super().__init__(to, mail['from_name'], mail['from_mail'], mail['subject'], datetime.strptime(mail['time'], '%Y-%m-%d %H:%M:%S'), proxies)
        self._letter_id = mail['mail_id']

    @property
    def letter(self):
        if self._letter:
            return self._letter
        r = requests.get(f'https://tempmail.plus/api/mails/{self._letter_id}?email={self._email}', proxies=self._proxies)
        if r.status_code == 200:
            self._letter = r.json()['text']
            return self._letter
