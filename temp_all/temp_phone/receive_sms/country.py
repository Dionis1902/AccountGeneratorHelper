from ..receive import country
from .phone import Phone
from ..exceptions import ProblemWithFetchNumbers
from bs4 import BeautifulSoup
import re


class Country(country.Country):
    def __init__(self, s, _country, url):
        super().__init__(s, _country, url)

    def get_numbers(self):
        if self._phones:
            return self._phones

        def __parse(page_number):
            r = self._s.get(self._url + f'{page_number}.html')
            if r.status_code != 200:
                raise ProblemWithFetchNumbers()
            page = BeautifulSoup(r.text, 'html.parser')
            try:
                _is_need_break = not page.find('ul', {'class': 'pagination'}).find_all('li')[-1].find('a').get('href', False)
            except AttributeError:
                _is_need_break = True

            return [Phone(self._s, self._country, e.find('a')['href'], re.findall(r'.*/(\d*)/', e.find('a')['href'])[0], page.find('h1').text.split()[-1]) for e in page.find_all('li', {'class': 'wow'})], \
                _is_need_break

        i = 0
        while True:
            i += 1
            data, is_need_break = __parse(i)
            self._phones += data
            if is_need_break:
                break
        return self._phones
