import asyncio
import random
import time
from datetime import datetime

from src.yandex.stoper import Stoper

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from src.yandex.yandex_check_modal import YandexCheckModal


class YandexInsertRequest:
    def __init__(self, driver):
        self.driver = driver
        self.count_write_wait = [0.1, 0.2, 1.3]

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

    def get_goog_search_element(self):
        try:
            elem = self.driver.find_element(by=By.XPATH, value=f"//form//input[contains(@class, 'input')]")

            return elem
        except:
            pass

        try:
            elem = self.driver.find_element(by=By.XPATH,
                                            value=f"//form//*[contains(@class, 'HeaderP')]/textarea")

            return elem
        except:
            pass

        return False

    def insert_request_to_search(self, _request):

        element_search = self.get_goog_search_element()

        if not element_search:
            return False

        time.sleep(1)

        for simbol in _request:
            element_search.send_keys(simbol)
            asyncio.run(Stoper().stoper(random.choices(self.count_write_wait)[0]))

        res_modal = YandexCheckModal(self.driver).start_check_modal()

        element_search.send_keys(Keys.ENTER)

        return True

    def loop_insert_search(self, _request):

        try:
            _request = _request.strip()
        except:
            pass

        count = 0
        count_try = 3

        while True:

            count += 1

            if count > count_try:
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'Не обнаружен запрос "{_request}')

                return False

            value_search = self.check_form_search()

            if value_search != _request:

                get_len = len(value_search)

                if get_len > 0:
                    self.loop_clear(get_len)

                res_insert_req = self.insert_request_to_search(_request)

                if count > 1:
                    time.sleep(1)

                continue

            return True
