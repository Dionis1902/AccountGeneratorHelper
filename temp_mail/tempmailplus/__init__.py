import random
import requests
from .letter import Letter
from ..exceptions import NotSetEmail
from ..mail import Mail
from .domains import Domains


class TempMailPlus(Mail):
    def __init__(self, proxy=None):
        super().__init__(proxy)

    def set_mail(self, mail, domain: Domains = None):
        if not domain:
            domain = Domains[random.choice(Domains._member_names_)]
        return super()._set_mail(mail + '@' + domain.value)

    def get_inbox(self):
        if not self._mail:
            raise NotSetEmail()

        r = requests.get(f'https://tempmail.plus/api/mails?email={self._mail}&limit=100')
        if r.status_code == 200:
            return [Letter(self._mail, _letter, self._proxies) for _letter in r.json()['mail_list']]
        return []