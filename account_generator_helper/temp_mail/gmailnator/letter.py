import json
import re
from ..mail import letter
from datetime import datetime

header_regex = r'<div id="subject-header"><b>From: <\/b>.*<br\/><b>Subject: <\/b>[^<]*<\/b><div><b>Time: <\/b>[^<]*<hr\s*\/><\/div><\/div>'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'content-type': 'application/json'
}


class Letter(letter.Letter):
    def __init__(self, to, content, proxies, token, session):
        self._token = token
        self._s = session
        letter_id, _from, subject = content['messageID'], content['from'], content['subject']
        super().__init__(to, *re.findall(r'(.*) <(.*)>', _from)[0], subject, datetime.fromtimestamp(0), proxies, letter_id)

    @property
    def letter(self):
        if self._letter:
            return self._letter
        payload = json.dumps({'email': self._email, 'messageID': self._letter_id})
        r = self._s.post('https://www.emailnator.com/message-list', proxies=self._proxies, data=payload,
                         headers={**headers, 'x-xsrf-token': self._token})
        if r.status_code == 200:
            self._letter = re.sub(header_regex, '', r.text)
            return self._letter
