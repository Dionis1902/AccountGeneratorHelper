import datetime
import re


class Letter:
    def __init__(self, mail, sender, subject, timestamp, proxies):
        self._mail = mail
        self._sender_name, self._sender_mail = re.findall(r'(.*) <(.*)>', sender)[0]
        self._subject = subject
        self._send_time = datetime.datetime.fromtimestamp(timestamp)
        self._proxies = proxies
        self._latter = None

    @property
    def mail(self):
        return self._mail

    @property
    def sender_name(self):
        return self._sender_name

    @property
    def sender_mail(self):
        return self._sender_mail

    @property
    def subject(self):
        return self._subject

    @property
    def send_time(self):
        return self._send_time

    @property
    def letter(self):
        return ''

    def __repr__(self):
        return '<Letter seder_name={} seder_mail={} mail={} subject={} send_time={}>'.format(self._sender_name,
                                                                                             self._sender_mail,
                                                                                             self._mail,
                                                                                             self._subject,
                                                                                             self._send_time.strftime('%Y-%m-%d %H:%M:%S'))

    def __hash__(self):
        return hash(self.__repr__())
