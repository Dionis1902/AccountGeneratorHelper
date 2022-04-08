import re
import requests
from ..mail import letter
from datetime import datetime
from account_generator_helper.utilities import unescape


class Letter(letter.Letter):
    def __init__(self, to, content, proxies):
        letter_id, _from, subject = re.findall(r'.*href="(https://www.gmailnator.com/inbox/.*)">.*<table.*<td.*>(.* <.*>)</td>.*<td.*>(.*)</td>.*<td.*>.*</td>.*', content.replace('\n', ''))[0]
        super().__init__(to, *re.findall(r'(.*) <(.*)>', _from)[0], subject, datetime.fromtimestamp(0), proxies)
        self._letter_id = letter_id

    @property
    def letter(self):
        if self._letter:
            return self._letter
        r = requests.get(self._letter_id, proxies=self._proxies)
        if r.status_code == 200:
            self._letter = unescape(r.text.split('iframe srcdoc="')[1].split('" id="message-body"')[0])
            return self._letter
