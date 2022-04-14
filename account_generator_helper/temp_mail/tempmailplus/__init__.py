import random
import requests
from .letter import Letter
from ..exceptions import NotSetEmail
from ..mail import Mail
from .tempmailplusdomains import TempMailPlusDomains


class TempMailPlus(Mail):
    """
    Class for work with https://tempmail.plus
    """
    def __init__(self, proxy=None):
        super().__init__(proxy)

    def set_email(self, email, domain: TempMailPlusDomains = None):
        """
        Use custom email address with custom domain.

        :param email: Email address.
        :param domain: Domain of email address, set None for random.
        :return: Email address.
        """

        if not domain:
            domain = TempMailPlusDomains[random.choice(TempMailPlusDomains._member_names_)]
        return super()._set_email(email + '@' + domain.value)

    def get_inbox(self):
        if not self._email:
            raise NotSetEmail()

        r = requests.get(f'https://tempmail.plus/api/mails?email={self._email}&limit=100')
        if r.status_code == 200:
            return [Letter(self._email, _letter, self._proxies) for _letter in r.json()['mail_list']]
        return []