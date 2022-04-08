import random

from ..countries import Counties
from .phone import Phone


class Country:
    def __init__(self, s, country, url):
        self._s = s
        self._country = Counties(country)
        self._url = url
        self._phones = []

    @property
    def country(self):
        """
        :return: Country.
        """
        return self._country

    def get_numbers(self) -> list[Phone]:
        """
        :return: List of phone numbers.
        """
        pass

    def __repr__(self):
        return '<Country country={}>'.format(self._country.name)

    def get_number(self):
        """
        :return: Random number.
        """
        return random.choice(self.get_numbers())
