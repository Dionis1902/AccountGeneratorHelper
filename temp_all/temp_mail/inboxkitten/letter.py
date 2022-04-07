import re
import requests
from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, url, headers, timestamp, proxies):
        super().__init__(headers['to'], *re.findall(r'(.*) <(.*)>', headers['from'])[0], headers['subject'], datetime.fromtimestamp(timestamp), proxies)
        self._letter_id = '-'.join(re.findall(r'https://(.*)\.api\.mailgun\.net/v3/domains/inboxkitten\.com/messages/(.*)', url)[0])

    @property
    def letter(self):
        if self._letter:
            return self._letter
        r = requests.get(f'https://inboxkitten.com/api/v1/mail/getHtml?mailKey={self._letter_id}', proxies=self._proxies)
        if r.status_code == 200:
            self._letter = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', r.text)
            return self._letter
