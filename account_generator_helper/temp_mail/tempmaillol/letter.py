from ..mail import letter
from datetime import datetime


class Letter(letter.Letter):
    def __init__(self, to, from_email, subject, timestamp, body):
        super().__init__(to, from_email, from_email, subject, datetime.fromtimestamp(timestamp / 1000))
        self.__body = body

    @property
    def letter(self):
        return self.__body
