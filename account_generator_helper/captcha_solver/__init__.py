import requests
import re


class CaptchaSolver:
    def __init__(self, proxy=None):
        self._s = requests.Session()
        if proxy:
            self._s.proxies.update({'http': proxy, 'https': proxy})
        self.__event_validation = None
        self.__view_state = None
        self.__save_data(self._s.get('https://cloudmersive.com/ocr-api').text)

    def __save_data(self, text):
        self.__event_validation = re.findall(r'__EVENTVALIDATION".*value="(.*)"', text)[0]
        self.__view_state = re.findall(r'__VIEWSTATE".*value="(.*)"', text)[0]

    @staticmethod
    def __get_captcha_result(text):
        result = re.findall(f'TextResult":.*"(.*)"', text)
        if result:
            return result[0].replace('\\n', '')
        return ''

    def solve(self, image: open) -> str:
        """
        Method for solving regular text captcha.

        :param image: open(file, 'rb')
        """
        data = {
            '__EVENTVALIDATION': self.__event_validation,
            '__VIEWSTATE': self.__view_state,
            'ctl00$MainContent$LanguageSelector': 'eng',
            'ctl00$MainContent$btnUpload2': 'Photos of Docs to Text'
        }

        r = self._s.post('https://cloudmersive.com/ocr-api', data=data, files={'ctl00$MainContent$FileUploadBox': image})
        if not r.ok:
            return ''
        self.__save_data(r.text)
        return self.__get_captcha_result(r.text)
