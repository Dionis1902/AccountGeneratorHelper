import random
import requests
from ..exceptions import ProblemWithGetEmail
from ..mail import Mail
from .gmailnatordomains import GmailNatorDomains
from account_generator_helper.utilities import random_string, quote
from .letter import Letter

headers = {
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


class GmailNator(Mail):
    """
    Class for work with https://www.gmailnator.com/
    """
    def __init__(self, proxy=None):
        super().__init__(proxy)
        self.__s = requests.Session()
        if proxy:
            self.__s.proxies.update(self._proxies)
        self.__s.get('https://www.gmailnator.com/')

    def __get_csrf_gmail_nator_token(self):
        return self.__s.cookies.get('csrf_gmailnator_cookie')

    def __get_payload(self, action, additional_data=''):

        return f'csrf_gmailnator_token={self.__get_csrf_gmail_nator_token()}&action={action}' + additional_data

    def get_email(self):
        return self.set_email(random_string(), GmailNatorDomains[random.choice(GmailNatorDomains._member_names_)])

    def get_email_online(self, use_custom_domain=True, use_plus=True, use_point=True):
        """
        Random email address from the site.

        :param use_custom_domain: Generate email not only from @gmail.com.
        :param use_plus: Generate email with "+" in address.
        :param use_point:  Generate email with "." in address.
        :return: Random email address.
        """

        payload = '&'.join(['', *[f"data[]={i+1}" for i, data in enumerate(list(locals().values())[1:]) if data]])
        r = self.__s.post('https://www.gmailnator.com/index/indexquery', headers=headers, data=self.__get_payload('GenerateEmail', payload))
        if r.status_code == 200:
            return self._set_email(r.json()['email'])
        raise ProblemWithGetEmail()

    def set_email(self, email, domain: GmailNatorDomains = GmailNatorDomains.GMAILNATOR_COM):
        return self._set_email(random.choice(domain.value).format(email))

    def get_inbox(self):
        payload = self.__get_payload('LoadMailList', f'&Email_address={quote(self._email)}')
        r = self.__s.post('https://www.gmailnator.com/mailbox/mailboxquery', headers=headers, data=payload)
        if r.status_code == 200:
            return [Letter(self._email, _letter['content'], self._proxies) for _letter in r.json() if 'inbox' in _letter['content']]
        return []
