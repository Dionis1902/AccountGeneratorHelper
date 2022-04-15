import re
from ..receive import Receive
from bs4 import BeautifulSoup
from ..exceptions import ProblemWithFetchNumbers
from .country import Country
from ...countries import Counties


class ReceiveSms(Receive):
    def __init__(self, proxy=None):
        super().__init__(proxy)

    def get_counties(self):
        if self._countries:
            return list(self._countries.items())

        def __parse(page_number):
            r = self._s.get(f'https://receive-sms-free.cc/regions/{page_number}.html')
            if r.status_code != 200:
                raise ProblemWithCounties()
            page = BeautifulSoup(r.text, 'html.parser')
            try:
                _is_need_break = not page.find('ul', {'class': 'pagination'}).find_all('li')[-1].find('a').get('href', False)
            except AttributeError:
                _is_need_break = True

            return [(re.findall(r'.*/(.*).png', e.find('img')['src'])[0].upper(), e.find('a')['href']) for e in page.find_all('li', {'class': 'wow'})], \
                _is_need_break

        i = 0
        while True:
            i += 1
            data, is_need_break = __parse(i)
            self._countries = {**self._countries, **{Counties(_country[0]): Country(self._s, *_country) for _country in data}}
            if is_need_break:
                break
        return list(self._countries.items())
