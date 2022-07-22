import json
import random
import requests
from ..exceptions import ProblemWithGetEmail
from ..mail import Mail
from account_generator_helper.utilities import random_string
from .letter import Letter
from urllib.parse import unquote

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'content-type': 'application/json'
}


class GmailNator(Mail):
    """
    Class for work with https://www.emailnator.com/
    """

    def __init__(self, proxy=None):
        super().__init__(proxy)
        self.__s = requests.Session()
        if proxy:
            self.__s.proxies.update(self._proxies)
        self.__s.get('https://www.emailnator.com/')

    def __get_xsrf_token(self):
        return unquote(self.__s.cookies.get('XSRF-TOKEN'))

    def get_email(self):
        return self.set_email(self.get_email_online())

    def get_email_online(self, use_custom_domain=True, use_plus=True, use_point=True):
        """
        Random email address from the site.

        :param use_custom_domain: Generate email not only from @gmail.com.
        :param use_plus: Generate email with "+" in address.
        :param use_point:  Generate email with "." in address.
        :return: Random email address.
        """
        data = ['domain', 'plusGmail', 'dotGmail']
        payload = json.dumps({'email': [i for i, k in zip(data, [use_custom_domain, use_plus, use_point]) if k]})
        r = self.__s.post('https://www.emailnator.com/generate-email',
                          headers={**headers, 'x-xsrf-token': self.__get_xsrf_token()}, data=payload)
        if r.status_code == 200:
            return self._set_email(r.json()['email'][0])
        raise ProblemWithGetEmail()

    def set_email(self, email):
        """
        Make sure you use the email address associated with this site or it won't work
        """
        return self._set_email(email)

    def get_inbox(self):
        payload = json.dumps({'email': self._email})
        r = self.__s.post('https://www.emailnator.com/message-list',
                          headers={**headers, 'x-xsrf-token': self.__get_xsrf_token()}, data=payload)
        if r.status_code == 200:
            return [Letter(self._email, _letter, self._proxies, self.__get_xsrf_token(), self.__s) for _letter in r.json()['messageData'] if
                    'ADS' not in _letter['messageID']]
        return []
