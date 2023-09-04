import asyncio
from datetime import datetime

from src.yandex.captcha_core import CoreCaptcha
from src.yandex.stoper import Stoper

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys


class YandexInsertRequest:
    def __init__(self, driver):
        self.driver = driver

    def check_form_search(self):
        try:
            value = self.driver.find_element(by=By.XPATH,
                                             value=f"//input[contains(@class, 'Form-Input')]").get_attribute(
                "value")

        except:
            return ''

        return value

    def loop_clear(self, count):
        for x in range(count):
            try:
                self.driver.find_element(by=By.XPATH,
                                 value=f"//input[contains(@class, 'Form-Input')]").send_keys(Keys.BACKSPACE)
            except:
                continue

        return True

    def loop_insert_search(self, _request):
        try:
            _request = _request.strip()
        except:
            pass

        count = 0
        count_try = 2

        while True:
            count += 1
            if count > count_try:
                print(f'Не обнаружен запрос "{_request}"')
                return False

            value_search = self.check_form_search()

            if value_search != _request:

                get_len = len(value_search)

                if get_len > 0:
                    self.loop_clear(get_len)

                res_insert_req = self.insert_quiest_search(row, request)

                if count > 1:
                    time.sleep(1)

                continue

            return True
