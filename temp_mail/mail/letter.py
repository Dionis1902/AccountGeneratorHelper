class Letter:
    def __init__(self, email, from_name, from_email, subject, send_time, proxies):
        self._email = email
        self._from_name = from_name
        self._from_email = from_email
        self._subject = subject
        self._send_time = send_time
        self._proxies = proxies
        self._latter = None

    @property
    def email(self):
        return self._email

    @property
    def from_name(self):
        return self._from_name

    @property
    def from_email(self):
        return self._from_email

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
        return '<Letter from_name={} from_email={} email={} subject={} send_time={}>'.format(self._from_name,
                                                                                             self._from_email,
                                                                                             self._email,
                                                                                             self._subject,
                                                                                             self._send_time.strftime('%Y-%m-%d %H:%M:%S'))

    def __hash__(self):
        return hash(self.__repr__())
