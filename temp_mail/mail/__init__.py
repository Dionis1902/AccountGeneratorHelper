import re
import time
from datetime import datetime
from ..utilities import random_string


class Mail:
    """
    Base class of mail service
    """
    def __init__(self, proxy=None):
        """
        :param proxy: (optional) Proxy string.
        """
        self._mail = None
        self._proxies = {'http': proxy, 'https': proxy} if proxy else None
        self._handlers = []

    def get_mail(self):
        """
        Generates a random address and returns it.

        :return: Random email address.
        :rtype: str
        """
        return self.set_mail(random_string())

    def set_mail(self, *args, **kwargs):
        pass

    def _set_mail(self, mail):
        self._mail = mail
        return self._mail

    def get_inbox(self):
        """
        Return all letters from inbox.

        :return: :class:`Letter <Letter>` object
        :rtype: temp_mail.mail.letter.Letter
        """
        pass

    def letter_handler(self, name='', from_email='', subject='', re_subject=''):
        """
        Letter handler decorator.
        This decorator can be used to decorate functions that must handle certain types of letters.
        All letters handlers are tested in the order they were added.

        :param name: (Optional) Name of the person who sent the letter.
        :param from_email: (Optional) Email address from which the letter was sent.
        :param subject: (Optional) Letter subject.
        :param re_subject: (Optional) The same as subject but use regular expression.
        """
        def wrapper(handler):
            self._handlers.append({'handler': handler, 'name': name, 'from_email': from_email,
                                   'subject': subject, 're_subject': re_subject,
                                   'time': datetime.now()})

        return wrapper

    def _letter_handler(self, _letter):
        def __is_valid(handler):
            return (not handler['name'] or handler['name'] == _letter.name) and \
                   (not handler['from_email'] or handler['from_email'] == _letter.from_email) and \
                   (not handler['subject'] or handler['subject'] == _letter.subject) and \
                   (not handler['re_subject'] or re.findall(handler['re_subject'], _letter.subject)) and \
                   (not handler['time'] or handler['time'] < _letter.send_time)

        for _handler in self._handlers:
            if __is_valid(_handler):
                _handler['handler'](_letter)

    def poling(self, timeout: int = 10):
        """
        Must use with letter_handler:

        :param timeout: (Optional) Timeout between inbox update, default 10 seconds.
        """
        letters = []
        try:
            while True:
                for _letter in self.get_inbox():
                    if hash(_letter) not in letters:
                        letters.append(hash(_letter))
                        self._letter_handler(_letter)
                time.sleep(timeout)
        except KeyboardInterrupt:
            pass
