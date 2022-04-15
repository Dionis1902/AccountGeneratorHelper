from ..receive import phone
from ..exceptions import ProblemWithFetchNumbers
from ..message import Message
from bs4 import BeautifulSoup


class Phone(phone.Phone):
    def __init__(self, s, country, url, number, code):
        super().__init__(s, country, url, number, code)

    def get_last_messages(self):
        data = []
        r = self._s.get(self._url)
        if r.status_code != 200:
            raise ProblemWithFetchMessages()

        page = BeautifulSoup(r.text, 'html.parser')
        table = page.find('div', {'class': 'casetext'})
        for e in table.find_all('div', {'class': 'row'})[1:]:
            try:
                data.append(Message(e.find('div', {'class': 'col-xs-12 col-md-2'}).find('div').text,
                                    e.find('div', {'class': 'col-xs-12 col-md-8'}).text,
                                    e.find('div', {'class': 'col-xs-0 col-md-2 mobile_hide'}).text))
            except AttributeError:
                pass
        return data
