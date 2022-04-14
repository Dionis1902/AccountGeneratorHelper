from account_generator_helper import Proxies

proxies = Proxies()
proxies.parse_proxies()

print(proxies)  # <Proxies proxies_count=11572>

print(proxies.pop())  # <Proxy proxy_type=HTTP address=203.23.106.209 port=80 country=Counties.CYPRUS>

print(proxies.pop().get())  # http://203.32.121.187:80