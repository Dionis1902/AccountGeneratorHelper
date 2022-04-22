import random
from .phone import Phone
from account_generator_helper.countries import Counties
from typing import List


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

    def get_numbers(self) -> List[Phone]:
        """
        :return: List of phone numbers.
        """
        pass

    def get_number(self) -> Phone:
        """
        :return: Random number.
        """
        return random.choice(self.get_numbers())

    def __repr__(self):
        return '<Country country={}>'.format(self._country.name)
