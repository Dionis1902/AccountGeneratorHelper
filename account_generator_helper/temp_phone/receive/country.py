import random
from .phone import Phone
from account_generator_helper.countries import Counties
from typing import List

from ..exceptions import NoNumbers


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
        numbers = self.get_numbers()
        if not numbers:
            raise NoNumbers()

        return random.choice(numbers)

    def __repr__(self):
        return '(Country country={})'.format(self._country.name)
