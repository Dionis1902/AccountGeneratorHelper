import logging
import random
import time
import requests
import selenium.common
from wit import Wit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from .exceptions import *
from .browser_options import options

client = Wit('JVHWCNWJLWLGN6MFALYLHAPKUFHMNTAC')


options.add_argument('--headless')


class AnyEc:
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                return fn(driver)
            except selenium.common.exceptions.NoSuchElementException:
                pass


class ReCaptchaSolver:
    def __init__(self, proxy=None):
        if proxy:
            options.add_argument('--proxy-server=%s' % proxy)
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=logging.CRITICAL).install()),
                                        options=options)

    @staticmethod
    def __wait(min_time, max_time):
        time.sleep(random.uniform(min_time, max_time))

    def __click(self, element):
        self._driver.execute_script('arguments[0].click();', element)

    def __send_keys(self, element, value):
        self._driver.execute_script(f'arguments[0].value = "{value}";', element)

    def __get_element(self, value, by=By.XPATH, timeout=10, until=EC.presence_of_element_located):
        return WebDriverWait(self._driver, timeout).until(until((by, value)))

    def __change_to_b_frame(self):
        self._driver.switch_to.default_content()
        self.__get_element('//iframe[contains(@src,"/bframe")]', until=EC.frame_to_be_available_and_switch_to_it)

    def __change_to_anchor(self):
        self._driver.switch_to.default_content()
        self.__get_element('//iframe[contains(@src,"/anchor")]', until=EC.frame_to_be_available_and_switch_to_it)

    def __open_captcha(self):
        self.__change_to_anchor()
        anchor = self.__get_element('recaptcha-anchor', by=By.ID, until=EC.element_to_be_clickable)
        self.__wait(0.5, 1.5)
        self.__click(anchor)

    def __open_audio_menu(self):
        self.__change_to_b_frame()
        audio_button = self.__get_element('recaptcha-audio-button', by=By.ID, until=EC.element_to_be_clickable)
        self.__wait(0.5, 1.5)
        self.__click(audio_button)

    def __get_url(self):
        self.__change_to_b_frame()
        element = WebDriverWait(self._driver, 10).until(AnyEc(
            EC.presence_of_element_located((By.CLASS_NAME, 'rc-doscaptcha-body-text')),
            EC.presence_of_element_located((By.ID, 'audio-source'))))

        if element.get_attribute('class') == 'rc-doscaptcha-body-text':
            raise GoogleDetectYouAreBot()

        element = self.__get_element('audio-source', by=By.ID, until=EC.presence_of_element_located)
        return element.get_attribute('src')

    def __get_text(self):
        r = requests.get(self.__get_url())
        return client.speech(r.content, {'Content-Type': 'audio/mpeg3'}).get('text', '')

    def __reload(self):
        old_url = self.__get_url()
        self.__click(self.__get_element('rc-button-reload', by=By.CLASS_NAME, until=EC.element_to_be_clickable))
        while True:
            if old_url != self.__get_url():
                break
            time.sleep(.5)

    def __check_error(self):
        try:
            element = self._driver.find_element(By.CLASS_NAME, 'error-code')
            if element.text in ('ERR_TIMED_OUT', 'ERR_EMPTY_RESPONSE', 'ERR_NO_SUPPORTED_PROXIES'):
                raise TimeOut()

        except selenium.common.exceptions.NoSuchElementException:
            pass

    def __is_solved(self):
        def _is_solved():
            try:
                self.__change_to_anchor()
                self._driver.find_element(By.XPATH, '//span[@id="recaptcha-anchor" and @aria-checked="true"]')
                return True
            except selenium.common.exceptions.NoSuchElementException:
                return False

        def _is_error():
            try:
                self.__change_to_b_frame()
                self._driver.find_element(By.CLASS_NAME, 'rc-response-input-field label-input-label rc-response-input-field-error')
                return True
            except selenium.common.exceptions.NoSuchElementException:
                return False

        for _ in range(10):
            is_solved, is_error = _is_solved(), _is_error()
            if is_solved:
                return True
            if is_error:
                return False
            time.sleep(1)
        return False

    def __get_response(self):
        self._driver.switch_to.default_content()
        return self.__get_element('g-recaptcha-response', by=By.NAME, until=EC.presence_of_element_located).get_attribute('value')

    def __open_audio_menu_and_check_solve(self):
        def _is_solve():
            try:
                self.__change_to_anchor()
                self._driver.find_element(By.XPATH, '//span[@id="recaptcha-anchor" and @aria-checked="true"]')
                return True
            except selenium.common.exceptions.NoSuchElementException:
                return False

        def _is_audio_button():
            try:
                self.__change_to_b_frame()
                self._driver.find_element(By.ID, 'recaptcha-audio-button')
                return True
            except selenium.common.exceptions.NoSuchElementException:
                return False

        for _ in range(10):
            is_solve, is_audio_button = _is_solve(), _is_audio_button()
            if is_solve:
                return True
            if is_audio_button:
                return False
            time.sleep(1)

    def __insert_captcha(self, site_key):
        self._driver.execute_script(f'document.body.innerHTML = "<div class=g-recaptcha data-sitekey={site_key}></div>";')
        self._driver.execute_script('document.head.innerHTML = "";')
        self._driver.execute_script('''let s = document.createElement('script');
                                       s.src = "https://www.google.com/recaptcha/api.js?hl=en";
                                       s.async = true;
                                       s.defer = true;
                                       document.head.appendChild(s);''')

    def solve(self, site_key=None, page_url=None):
        self._driver.get(page_url)

        self.__insert_captcha(site_key)

        self.__check_error()

        self.__open_captcha()

        if self.__open_audio_menu_and_check_solve():
            return self.__get_response()

        self.__open_audio_menu()

        for _ in range(5):
            while True:
                text = self.__get_text()
                if text:
                    break
                self.__reload()
            audio_response = self.__get_element('audio-response', by=By.ID, until=EC.presence_of_element_located)
            self.__send_keys(audio_response, text)
            verify_button = self.__get_element('recaptcha-verify-button', by=By.ID, until=EC.element_to_be_clickable)
            self.__wait(0.5, 1.5)
            self.__click(verify_button)

            self._driver.switch_to.default_content()
            self.__get_element('//iframe[contains(@src,"/anchor")]', until=EC.frame_to_be_available_and_switch_to_it)
            if self.__is_solved():
                break
        else:
            return None
        return self.__get_response()

    def close(self):
        self._driver.quit()
