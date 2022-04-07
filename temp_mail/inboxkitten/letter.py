import datetime
import re
import requests


class Letter:
    def __init__(self, url, headers, timestamp, proxies):
        self.__mail = headers['to']
        self.__letter_id = '-'.join(re.findall(r'https://(.*)\.api\.mailgun\.net/v3/domains/inboxkitten\.com/messages/(.*)', url)[0])
        self.__seder_name, self.__sender_mail = re.findall(r'(.*) <(.*)>', headers['from'])[0]
        self.__subject = headers['subject']
        self.__send_time = datetime.datetime.fromtimestamp(timestamp)
        self.__proxies = proxies
        self.__latter = None

    @property
    def mail(self):
        return self.__mail

    @property
    def seder_name(self):
        return self.__seder_name

    @property
    def sender_mail(self):
        return self.__sender_mail

    @property
    def subject(self):
        return self.__subject

    @property
    def send_time(self):
        return self.__send_time

    @property
    def letter(self):
        if self.__latter:
            return self.__latter
        r = requests.get(f'https://inboxkitten.com/api/v1/mail/getHtml?mailKey={self.__letter_id}', proxies=self.__proxies)
        if r.status_code == 200:
            self.__latter = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', r.text)
            return self.__latter

    def __repr__(self):
        return '<Letter seder_name={} seder_mail={} mail={} subject={} send_time={}>'.format(self.__seder_name,
                                                                                             self.__sender_mail,
                                                                                             self.__mail,
                                                                                             self.__subject,
                                                                                             self.__send_time.strftime('%Y-%m-%d %H:%M:%S'))

    def __hash__(self):
        return hash(self.__repr__())
