import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from settings import NAME_SERVER
from src.google.google_core import ConnectGoogleCore
from src.telegram_debug import SendlerOneCreate
from src.yandex.load_page import LoadPage
from src.yandex.sms_activate_api import SmsActivateApi
from src.yandex.yandex_gen_accont_date import YandexAccaunt


class _BoosterFarmAcc:
    def __init__(self, google_alternate, dir_project, android_phone, driver, status, login_password):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone
        self.driver = driver
        self.status = status
        self.login_password = login_password

        self._count_tile_wait = [0.1, 0.2, 1.3]

        self._big_wait = [62, 73, 87, 68, 51]

        self.list_shab = {
            0: self.one_farm,
            1: self.two_farm
        }

    def one_farm(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: запуск шаблона №1 для прогрева аккаунтов')

        url = 'https://mail.yandex.ru'

        res_load = LoadPage(self.driver, url, self.dir_project).loop_load_page("//*[contains(text(), 'Яндекс')]")

        if not res_load:
            return False

        time.sleep(random.choices(self._big_wait)[0])

        return True

    def two_farm(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: запуск шаблона №2 для прогрева аккаунтов')

        _req = YandexAccaunt.gen_request()

        url = f'https://yandex.ru/search/?text={_req}'

        res_load = LoadPage(self.driver, url, self.dir_project).loop_load_page("//*[contains(text(), 'Яндекс')]")

        if not res_load:
            return False

        time.sleep(random.choices(self._big_wait)[0])

        return True

    def loop_write_in_cell(self, name_sheet, account_row, columns, over_status):

        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                SendlerOneCreate('').save_text(f'{NAME_SERVER} BoosterSeo: Не смог записать в столбец {columns} '
                                               f'в строчку "{account_row}" farm')

                return False

            res_write = self.google_alternate.new_write_in_cell(name_sheet, account_row, columns, over_status)

            if not res_write:
                self.google_alternate = ConnectGoogleCore()

                continue

            return res_write

    def start_farm(self, account_row):

        res = self.list_shab[random.choice([x for x in self.list_shab.keys()])]()

        over_status = self.status + 1

        self.loop_write_in_cell('аккаунты', account_row, 4, over_status)

        time.sleep(1)

        self.loop_write_in_cell('аккаунты', account_row, 6, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return True
