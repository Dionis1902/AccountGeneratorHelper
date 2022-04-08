import random
import re
import string
from urllib.parse import quote
from datetime import timedelta

try:
    from html import unescape
except ImportError:
    from html.parser import HTMLParser
    unescape = HTMLParser().unescape

LETTERS = string.ascii_letters + '1234567890'


def random_string():
    return ''.join([random.choice(LETTERS) for _ in range(12)])


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


def camel_to_snake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
