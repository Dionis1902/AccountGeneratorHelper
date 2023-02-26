from .letter import Letter
from ..exceptions import NotSetEmail, ProblemWithGetEmail
from ..mail import Mail


class TempMailLol(Mail):
    """
    Class for work with https://tempmail.lol/
    """

    def __init__(self, proxy=None):
        super().__init__(proxy)
        self.__token = None

    def get_email(self, community_addresses: bool = True):
        """
        Get random email address from https://tempmail.lol/

        :community_addresses: Community addresses use domains people have given to the website
        """
        r = self._s.get('https://api.tempmail.lol/generate/rush' if community_addresses else 'https://api.tempmail.lol/generate')
        if not r.ok:
            raise ProblemWithGetEmail()
        self.__token = r.json()['token']
        return self.set_email(r.json()['address'])

    def get_inbox(self):
        if not self._email or not self.__token:
            raise NotSetEmail()

        r = self._s.get(f'https://api.tempmail.lol/auth/{self.__token}')
        if r.status_code == 200:
            return [Letter(_letter['to'], _letter['from'],  _letter['subject'], _letter['date'], _letter['body']) for _letter in r.json().get('email', [])]
        return []
