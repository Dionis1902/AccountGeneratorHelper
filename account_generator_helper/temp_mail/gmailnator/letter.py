import json
import re
from ..mail import letter
from datetime import datetime

header_regex = r'<div id="subject-header"><b>From: <\/b>.*<br\/><b>Subject: <\/b>[^<]*<\/b><div><b>Time: <\/b>[^<]*<hr\s*\/><\/div><\/div>'
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "content-type": "application/json",
}


class Letter(letter.Letter):
    def __init__(self, to, content, token, session):
        self._token = token
        self._s = session
        if "<" in content["from"]:
            name, from_email = re.findall(r"^(.*) <(.*)>$", content["from"])[0]
        else:
            name = from_email = content["from"]
        super().__init__(
            to,
            name,
            from_email,
            content["subject"],
            datetime.fromtimestamp(0),
            content["messageID"],
        )

    @property
    def letter(self):
        if self._letter:
            return self._letter
        payload = json.dumps({"email": self._email, "messageID": self._letter_id})
        r = self._s.post(
            "https://emailnator.com/message-list",
            data=payload,
            headers={**headers, "x-xsrf-token": self._token},
        )
        if r.status_code == 200:
            self._letter = re.sub(header_regex, "", r.text)
            return self._letter
