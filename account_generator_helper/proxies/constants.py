import enum


class ProxyType(enum.Enum):
    HTTP = 'http'
    HTTPS = 'http'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5'
