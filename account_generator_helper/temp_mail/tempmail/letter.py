import re

from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, to, from_email, subject, timestamp, body):
        if '<' in from_email:
            name, from_email = re.findall(r'^(.*) <(.*)>$', from_email)[0]
        else:
            name = from_email = from_email

        super().__init__(to, name, from_email, subject, datetime.fromtimestamp(timestamp))
        self.__body = body

    @property
    def letter(self):
        return self.__body
