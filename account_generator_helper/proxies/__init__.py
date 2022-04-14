import re
import requests
from .constants import ProxyType
from account_generator_helper.proxies.proxy import Proxy
from ..countries import Counties
from threading import Thread, Lock
from bs4 import BeautifulSoup


class Proxies:
    __lock = Lock()

    def __init__(self):
        self.__proxies: list[Proxy] = []

    def _proxy_list(self):
        for proxy_type in ProxyType:
            r = requests.get(f'https://www.proxy-list.download/api/v1/get?type={proxy_type.value}')
            if not r.ok:
                continue
            for row in r.text.split():
                with self.__lock:
                    self.__proxies.append(Proxy(proxy_type, *row.split(':'), None))

    def _ssl_proxies(self):
        for proxy_type, url in zip([ProxyType.HTTPS, ProxyType.SOCKS4], ['https://www.sslproxies.org/', 'https://www.socks-proxy.net/']):
            resp = requests.get(url)
            for row in self._re_proxy(resp.text):
                address, port, country = row
                try:
                    country = Counties(country.upper())
                except ValueError:
                    country = None
                with self.__lock:
                    self.__proxies.append(Proxy(proxy_type, address, port, country))

    def _hide_me(self):
        i = 0
        while True:
            r = requests.get(f'https://hidemy.name/ua/proxy-list/?start={i * 64}#list', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'})
            if not r.ok:
                continue
            page = BeautifulSoup(r.text, 'html.parser')
            table = page.find('tbody')
            if not table:
                continue
            for row in table.find_all('tr'):
                address, port, country, _, proxy_type, _, _ = row.find_all('td')
                try:
                    country = getattr(Counties, '_'.join(country.find('span', {'class': 'country'}).text.split(', ')[::-1]).replace(' ', '_').upper())
                except AttributeError:
                    country = None
                with self.__lock:
                    self.__proxies.append(Proxy(getattr(ProxyType, proxy_type.text.split(',')[0].upper()),
                                                address.text, port.text, country))
            if page.find('div', {'class': 'pagination'}).find_all('a')[-1].text.isdigit():
                break
            i += 1

    @staticmethod
    def _re_proxy(string):
        for row in re.findall(r'<td>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})</td><td>([0-9]{2,5})</td><td>(\D{2})</td>', string):
            yield row

    @property
    def proxies(self) -> list[Proxy]:
        return self.__proxies

    def __worker(self, proxies, good_proxies):
        while proxies:
            __proxy = None
            with self.__lock:
                __proxy = proxies.pop()
            status = __proxy.is_valid()
            if status:
                with self.__lock:
                    good_proxies.append(__proxy)

    def parse_proxies(self):
        """
        Method for parsing all proxies from all services.
        """
        parsers = [self._proxy_list, self._ssl_proxies, self._hide_me]
        threads = [Thread(target=parser, daemon=True) for parser in parsers]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

    def test_proxies(self, workers_count=100):
        """
        Method for testing all proxies and saving only working proxies.

        :param workers_count: Threads count.
        """
        testing_proxies, good_proxies = self.__proxies.copy(), []
        threads = [Thread(target=self.__worker, args=(testing_proxies, good_proxies), daemon=True) for _ in range(workers_count)]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        self.__proxies = good_proxies

    def pop(self, index=-1) -> Proxy:
        """
        Remove and return item at index (default last).

        :param index: Index by which to remove and return proxy.
        :return: proxy object.
        """
        with self.__lock:
            return self.__proxies.pop(index)

    def __len__(self):
        return len(self.__proxies)

    def __iter__(self):
        return iter(self.__proxies)

    def __repr__(self):
        return '<Proxies proxies_count={proxies_count}>'.format(proxies_count=len(self.__proxies))
