from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, to, mail, session):
        super().__init__(to, mail['from_name'], mail['from_mail'], mail['subject'], datetime.strptime(mail['time'], '%Y-%m-%d %H:%M:%S'))
        self._letter_id = mail['mail_id']
        self._s = session

    @property
    def letter(self):
        if self._letter:
            return self._letter
        r = self._s.get(f'https://tempmail.plus/api/mails/{self._letter_id}?email={self._email}')
        if r.status_code == 200:
            self._letter = r.json()['text']
            return self._letter
