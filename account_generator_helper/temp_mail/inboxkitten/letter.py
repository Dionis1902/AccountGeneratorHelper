import re
from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, url, headers, timestamp, session):
        if '<' in headers['from']:
            name, from_email = re.findall(r'(.*) <(.*)>', headers['from'])[0]
        else:
            name = from_email = headers['from']
        super().__init__(headers['to'], name, from_email, headers['subject'], datetime.fromtimestamp(timestamp))
        self._letter_id = '-'.join(re.findall(r'https://(.*)\.api\.mailgun\.net/v3/domains/inboxkitten\.com/messages/(.*)', url)[0])
        self._s = session

    @property
    def letter(self):
        if self._letter:
            return self._letter
        r = self._s.get(f'https://inboxkitten.com/api/v1/mail/getHtml?mailKey={self._letter_id}')
        if r.status_code == 200:
            self._letter = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', r.text)
            return self._letter
