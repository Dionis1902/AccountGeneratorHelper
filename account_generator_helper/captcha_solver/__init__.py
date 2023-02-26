import requests

from account_generator_helper.captcha_solver.exceptions import CantRecognize, DailyLimit


class CaptchaSolver:
    def __init__(self, api_key):
        self.__api_key = api_key

    def solve(self, image: open) -> str:
        """
        Method for solving regular text captcha.

        :param image: open(file, 'rb')

        :result: Captcha text
        """
        r = requests.post('https://api.optiic.dev/process', params={'apiKey': self.__api_key}, files={'image': image})
        if r.status_code == 429:
            raise DailyLimit()
        if not r.ok or not r.json().get('text'):
            raise CantRecognize()
        return r.json()['text']
