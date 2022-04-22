from ..message import Message
from typing import List


class Phone:
    def __init__(self, s, country, url, number, code):
        self._s = s
        self._country = country
        self._url = url
        self._number = number
        self._code = code

    @property
    def country(self):
        """
        :return: Country of phone number.
        """
        return self._country

    @property
    def number(self):
        """
        :return: Phone number.
        """
        return self._number

    def get_last_messages(self) -> List[Message]:
        """
        :return: List of Message objects.
        """
        pass

    def __repr__(self):
        return '<Phone code={} number=+{} country={}>'.format(self._code, self._number, self._country.name)
