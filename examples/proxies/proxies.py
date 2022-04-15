import sys

from account_generator_helper import Proxies
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                              '%m-%d-%Y %H:%M:%S')
logging.getLogger('urllib3.connectionpool').propagate = False
logging.getLogger('socks').propagate = False

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)


proxies = Proxies()

proxies.parse_proxies()

print(proxies)  # <Proxies proxies_count=11572>

print(proxies.pop())  # <Proxy proxy_type=HTTP address=203.23.106.209 port=80 country=Counties.CYPRUS>

print(proxies.pop().strfproxy())  # http://203.32.121.187:80
