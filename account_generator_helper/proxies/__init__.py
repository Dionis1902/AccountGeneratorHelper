import json
import re
import requests
from .constants import ProxyType
from account_generator_helper.proxies.proxy import Proxy
from ..countries import Counties
from threading import Thread, Lock
from bs4 import BeautifulSoup
import logging
import base64
from typing import List


class Proxies:
    __lock = Lock()

    def __init__(self):
        self.__proxies: set[Proxy] = set()
        self.__logger = logging.getLogger('AccountGeneratorHelper')

    def _proxy_list(self, _):
        urls = [
            ('https://www.proxy-list.download/api/v1/get?type=http', ProxyType.HTTPS),
            ('https://www.proxy-list.download/api/v1/get?type=socks4', ProxyType.SOCKS4),
            ('https://www.proxy-list.download/api/v1/get?type=socks5', ProxyType.SOCKS5),
            ('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', ProxyType.HTTP),
            ('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all', ProxyType.SOCKS4),
            ('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all', ProxyType.SOCKS5)
        ]

        for url, proxy_type in urls:
            r = requests.get(url)
            if not r.ok:
                continue
            proxies = r.text.split()
            self.__logger.debug('{} parsed {} {} proxy'.format(url.split('/api/')[0].split('/v')[0], len(proxies), proxy_type.name))
            for row in proxies:
                with self.__lock:
                    self.__proxies.add(Proxy(proxy_type, *row.split(':'), None))

    def _ssl_proxies(self, _):
        for proxy_type, url in zip([ProxyType.HTTP, ProxyType.HTTPS, ProxyType.SOCKS4], ['https://free-proxy-list.net', 'https://www.sslproxies.org', 'https://www.socks-proxy.net']):
            resp = requests.get(url)
            proxies = self._re_proxy(resp.text)
            self.__logger.debug('{} parsed {} proxy'.format(url, len(proxies)))
            for row in proxies:
                address, port, country = row
                try:
                    country = Counties(country.upper())
                except ValueError:
                    country = None
                with self.__lock:
                    self.__proxies.add(Proxy(proxy_type, address, port, country))

    def _hide_me(self, max_page):
        i = 0
        while True:
            r = requests.get(f'https://hidemy.name/ua/proxy-list/?start={i * 64}#list', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'})
            if not r.ok:
                continue
            page = BeautifulSoup(r.text, 'html.parser')
            table = page.find('tbody')
            if not table:
                continue
            proxies_rows = table.find_all('tr')
            for row in proxies_rows:
                address, port, country, _, proxy_type, _, _ = row.find_all('td')
                try:
                    country = getattr(Counties, '_'.join(country.find('span', {'class': 'country'}).text.split(', ')[::-1]).replace(' ', '_').upper())
                except AttributeError:
                    country = None
                with self.__lock:
                    self.__proxies.add(Proxy(getattr(ProxyType, proxy_type.text.split(',')[0].upper()),
                                                address.text, port.text, country))

            self.__logger.debug('https://hidemy.name page {} parsed {} proxy'.format(i+1, len(proxies_rows)))
            if page.find('div', {'class': 'pagination'}).find_all('a')[-1].text.isdigit():
                break
            if max_page and max_page == i:
                break
            i += 1

    def _geo_node(self, _):
        r = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=100000&page=1&sort_by=lastChecked&sort_type=desc')
        if not r.ok:
            return
        data = r.json().get('data', [])
        self.__logger.debug('https://geonode.com parsed {} proxy'.format(len(data)))
        for row in data:
            try:
                country = Counties(row['country'])
            except ValueError:
                country = None

            with self.__lock:
                self.__proxies.add(Proxy(ProxyType(row['protocols'][0] if row['protocols'][0] != 'https' else 'http'),
                                         row['ip'], row['port'], country))

    def _advanced(self, max_page):
        i = 1
        while True:
            r = requests.get(f'https://advanced.name/freeproxy?page={i}')
            if not r.ok:
                continue
            page = BeautifulSoup(r.text, 'html.parser')
            table = page.find('tbody')
            if not table:
                continue
            proxies_rows = table.find_all('tr')
            for row in proxies_rows:
                _, address, port, proxy_type, country, _, _ = row.find_all('td')
                try:
                    country = Counties(country.find('a').text)
                except (AttributeError, ValueError):
                    country = None

                with self.__lock:
                    try:
                        self.__proxies.add(Proxy(getattr(ProxyType, proxy_type.find('a').text.upper()),
                                                 base64.b64decode(address['data-ip']).decode(),
                                                 base64.b64decode(port['data-port']).decode(), country))
                    except AttributeError:
                        pass
            self.__logger.debug('https://advanced.name page {} parsed {} proxy'.format(i + 1, len(proxies_rows)))
            if page.find('ul', {'class': 'pagination pagination-lg'}).find_all('a')[-2].text == str(i):
                break
            if max_page and max_page == i:
                break
            i += 1

    def _open_proxy(self, _):
        urls = [
            ('https://openproxy.space/list/http', ProxyType.HTTP),
            ('https://openproxy.space/list/socks4', ProxyType.SOCKS4),
            ('https://openproxy.space/list/socks5', ProxyType.SOCKS5)
        ]
        for url, proxy_type in urls:
            r = requests.get(url)
            if not r.ok:
                continue
            self.__logger.debug('https://openproxy.space parsed {} {} proxy'.format(re.findall('<div class="amount">(\d*)</div>', r.text)[0], proxy_type.name))
            data = re.findall(r'return \{.*data:(\[\{.*\}\]),added', r.text)[0]
            for i in [r',active:\D', r',count:\D']:
                data = re.sub(i, '', data)
            for i in ['items', 'count', 'code']:
                data = data.replace(i, f'"{i}"')
            for main_data in json.loads(data):
                try:
                    country = Counties(main_data['code'])
                except (AttributeError, ValueError):
                    country = None

                for item in main_data.get('items', []):
                    with self.__lock:
                        self.__proxies.add(Proxy(proxy_type, *item.split(':'), country))

    @staticmethod
    def _re_proxy(string):
        return re.findall(r'<td>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})</td><td>([0-9]{2,5})</td><td>(\D{2})</td>', string)

    @property
    def proxies(self) -> List[Proxy]:
        return list(self.__proxies)

    def __worker(self, proxies, good_proxies, info):
        while proxies:
            __proxy = None
            with self.__lock:
                __proxy = proxies.pop()
            is_valid = __proxy.is_valid()
            with self.__lock:
                info[0] -= 1
                if is_valid:
                    good_proxies.add(__proxy)
                self.__logger.debug(
                    '{proxy} is {valid}, valid proxy counts = {valid_proxy_counts}, need to test {need_to_test} proxy'.format(
                        proxy=__proxy.strfproxy(), valid='valid' if is_valid else 'not valid',
                        valid_proxy_counts=len(good_proxies), need_to_test=info[0]
                    ))

    def parse_proxies(self, max_page=0):
        """
        Method for parsing all proxies from all services.

        :param max_page: Maximum number of pages from which you need to parse the proxy, 0 if you need to parse all.
        """
        self.__logger.debug('Start parsing proxy')
        parsers = [self._proxy_list, self._ssl_proxies, self._hide_me, self._geo_node, self._advanced, self._open_proxy]
        threads = [Thread(target=parser, args=(max_page, ), daemon=True) for parser in parsers]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        self.__logger.debug('Success parsed {} proxy'.format(len(self.__proxies)))

    def test_proxies(self, workers_count=100):
        """
        Method for testing all proxies and saving only working proxies.

        :param workers_count: Threads count.
        """
        self.__logger.debug(f'Start testing proxy, workers count = {workers_count}')
        testing_proxies, good_proxies = list(self.__proxies).copy(), set()
        info = [len(testing_proxies)]
        threads = [Thread(target=self.__worker, args=(testing_proxies, good_proxies, info), daemon=True) for _ in range(workers_count)]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        self.__proxies = good_proxies
        self.__logger.debug('Success tested proxy, count of valid proxy {}'.format(len(self.__proxies)))

    def pop(self) -> Proxy:
        """
        Remove and return item at index (default last).

        :return: proxy object.
        """
        with self.__lock:
            return self.__proxies.pop()

    def dump(self, file: open):
        file.write('\n'.join(map(str, self.__proxies)))

    def load(self, file: open):
        data = re.findall(r'(http|socks4|socks5)://(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{2,5})', file.read())
        [self.__proxies.add(Proxy(ProxyType(proxy_type), address, int(port), None)) for proxy_type, address, port in data]

    def __len__(self):
        return len(self.__proxies)

    def __iter__(self):
        return iter(self.__proxies)

    def __repr__(self):
        return '<Proxies proxies_count={proxies_count}>'.format(proxies_count=len(self.__proxies))
