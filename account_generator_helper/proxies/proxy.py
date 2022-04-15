from json import JSONDecodeError
import requests
from ..countries import Counties


class Proxy:
    def __init__(self, proxy_type, address, port, country):
        self._proxy_type = proxy_type
        self._address = address
        self._port = int(port)
        self._country = country

    @property
    def proxy_type(self):
        return self._proxy_type

    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port

    @property
    def country(self):
        return self._country

    def strfproxy(self, str_format='{proxy_type}://{address}:{port}') -> str:
        """
        Return formatted proxy string.
        {proxy_type} - Proxy type
        {address} - Proxy address
        {port} - Port address

        :param str_format: Example {proxy_type}://{address}:{port}
        :return:
        """
        return str_format.format(proxy_type=self.proxy_type.value, address=self._address, port=self._port)

    def is_valid(self, timeout=10) -> bool:
        """
        Testing proxy.

        :param timeout: Max timeout, default 10 seconds
        :return: bool
        """
        try:
            r = requests.get("http://ip-api.com/json?fields=countryCode", proxies={'http': self.strfproxy(), 'https': self.strfproxy()}, timeout=timeout)
            try:
                self._country = Counties(r.json()['countryCode'])
            except JSONDecodeError:
                return False
            except (ValueError, KeyError):
                self._country = None
        except IOError:
            return False
        return True

    def __repr__(self):
        return '<Proxy proxy_type={proxy_type} address={address} port={port} country={country}>'.format(
            proxy_type=self.proxy_type.name, address=self._address, port=self._port,
            country=self._country)

    def __hash__(self):
        return hash(self.strfproxy())

    def __eq__(self, other):
        return self.__str__() == str(other)

    def __ne__(self, other):
        return self.__str__() != str(other)

    def __str__(self):
        return self.strfproxy()