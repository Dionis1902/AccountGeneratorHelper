import requests
from .exceptions import ProblemWithGetPersonData
from .personcounties import PersonCounties
from ..utilities import camel_to_snake

headers = {
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


class Person:
    def __init__(self):
        self._name = None
        self._phone = None
        self._postcode = None
        self._street_address = None
        self._city = None
        self._country = None

        self.update_data()

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @property
    def postcode(self):
        return self._postcode

    @property
    def street_address(self):
        return self._street_address

    @property
    def country(self):
        return self._country

    def update_data(self, country: PersonCounties = PersonCounties.USA):
        """
        Generate new person data.

        :param country: From which country the street.
        """
        r = requests.post('https://www.textreverse.com/frontend/fakeAddressGenerator', data=f'lang={country.value}', headers=headers)
        if r.status_code != 200:
            raise ProblemWithGetPersonData()

        [setattr(self, '_' + camel_to_snake(key), r.json()[0][key]) for key in r.json()[0] if
         self.__getattr('_' + camel_to_snake(key))]

    def __getattr(self, key):
        try:
            getattr(self, key)
            return True
        except AttributeError:
            return False

    def __repr__(self):
        return '<Person {}>'.format(' '.join(['{}={}'.format(key[1:], value) for key, value in zip(vars(self).keys(), vars(self).values())]))


