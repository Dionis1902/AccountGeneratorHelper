import requests
from .letter import Letter
from ..exceptions import NotSetEmail
from ..mail import Mail


class InboxKitten(Mail):
    """
    Class for work with https://inboxkitten.com/
    """
    def __init__(self, proxy=None):
        super().__init__(proxy)

    def set_email(self, email):
        """
        Use custom email address.

        :param email: Email address.
        :return: Email address.
        :rtype: str
        """
        return super()._set_email(email) + '@inboxkitten.com'

    def get_inbox(self):
        if not self._email:
            raise NotSetEmail()

        r = requests.get(f'https://inboxkitten.com/api/v1/mail/list?recipient={self._email}', proxies=self._proxies)
        if r.status_code == 200:
            return [Letter(__letter['storage']['url'], __letter['message']['headers'], __letter['timestamp'],
                           self._proxies) for __letter in r.json()]
        return []
