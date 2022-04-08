import random
import requests
from .country import Country
from ..countries import Counties

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}


class Receive:
    def __init__(self, proxy):
        self._s = requests.Session()
        if proxy:
            self._s.proxies.update({'http': proxy, 'https': proxy})
        self._s.headers.update(headers)
        self._countries = []

    def get_counties(self) -> list[Country]:
        """
        :return: List of counties.
        """
        pass

    def get_country(self, country: Counties) -> Country:
        """
        Method returns object of the country, from this object you can get the phone number of this country.

        :param country: Country.
        :return: Country object.
        """
        return dict(enumerate(filter(lambda x: x.country == country, self.get_counties()))).get(0, None)

    def get_random_country(self):
        """
        :return: Random Country object.
        """
        return random.choice(self.get_counties())
