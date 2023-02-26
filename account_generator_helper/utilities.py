import random
import string
from datetime import timedelta

try:
    from html import unescape
except ImportError:
    from html.parser import HTMLParser
    unescape = HTMLParser().unescape


def random_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(12)])


def str_to_timedelta(string_time):
    _time = int(string_time.split()[0])
    if 'second' in string_time:
        return timedelta(seconds=_time)
    elif 'min' in string_time:
        return timedelta(minutes=_time)
    elif 'hour' in string_time:
        return timedelta(hours=_time)
    elif 'day' in string_time:
        return timedelta(days=_time)
    elif 'month' in string_time:
        return timedelta(days=_time*30)
    elif 'year' in string_time:
        return timedelta(days=_time*365)
    return timedelta()


