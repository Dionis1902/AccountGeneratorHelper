import requests
from temp_mail.inboxkitten.letter import Letter
from temp_mail.exceptions import NotSetEmail
from ..mail import Mail


class InboxKitten(Mail):
    def __init__(self, proxy=None):
        super().__init__(proxy)

    def set_mail(self, mail):
        return super().set_mail(mail) + '@inboxkitten.com'

    def get_inbox(self) -> list[Letter]:
        if not self._mail:
            raise NotSetEmail()

        r = requests.get(f'https://inboxkitten.com/api/v1/mail/list?recipient={self._mail}', proxies=self._proxies)
        if r.status_code == 200:
            letters = [Letter(__letter['storage']['url'], __letter['message']['headers'], __letter['timestamp'],
                              self._proxies) for __letter in r.json()]
            return letters
        return []

