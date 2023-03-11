import cloudscraper

from .letter import Letter
from ..exceptions import NotSetEmail, ProblemWithGetEmail
from ..mail import Mail


class TempMail(Mail):
    """
    Class for work with https://temp-mail.org/
    """

    def __init__(self, proxy=None):
        super().__init__(proxy)

        self._s = cloudscraper.create_scraper(delay=10, browser="chrome")
        if proxy:
            self._s.proxies.update(self._proxies)

        self.__token = None

    def get_email(self):
        """
        Get random email address from https://temp-mail.org/
        """

        r = (self._s.get if self.__token else self._s.post)('https://web2.temp-mail.org/mailbox',
                                                            headers={'Authorization': 'Bearer ' + self.__token} if self.__token else None)
        if not r.ok:
            raise ProblemWithGetEmail()
        if not self.__token:
            self.__token = r.json().get('token')
        return self.set_email(r.json()['mailbox'])

    def get_inbox(self):
        if not self._email or not self.__token:
            raise NotSetEmail()

        r = self._s.get(f'https://web2.temp-mail.org/messages', headers={'Authorization': 'Bearer ' + self.__token})
        if r.ok:
            return [Letter(self._email, _letter['from'],  _letter['subject'], _letter['receivedAt'], _letter['bodyPreview']) for _letter in r.json().get('messages', [])]
        return []
