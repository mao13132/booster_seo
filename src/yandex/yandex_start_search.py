import asyncio
import random
import time
from datetime import datetime
from time import perf_counter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.telegram_debug import SendlerOneCreate
from src.yandex.load_page import LoadPage
from src.yandex.stoper import Stoper
from src.yandex.yandex_check_modal import YandexCheckModal
from src.yandex.yandex_insert_request import YandexInsertRequest
from src.yandex.yandex_loop_page import YandexLoopPage


class YandexFarmSearch:
    def __init__(self, driver, name_profile, target_request, dir_project, google_alternate):
        self.driver = driver

        self.msg = f'Аккаунт: "{name_profile}"'

        self.url = 'https://yandex.ru/search'

        self.target_request = target_request

        self.count_try = 3

        self.dir_project = dir_project

        self.google_alternate = google_alternate

        self.name_profile = name_profile

    def write_request(self):

        count = 0

        while True:
            count += 1

            if count > self.count_try:
                SendlerOneCreate('').save_text(f'Израсходовал все попытки ввести запрос "{self.target_request}"')
                return False

            print(f'{self.msg} Начинаю обработку ключевика "{self.target_request}"')

            res_insert_request = YandexInsertRequest(self.driver).loop_insert_search(self.target_request)

            if res_insert_request:
                return True

            time.sleep(2)

            res_load = LoadPage(self.driver, self.url, self.dir_project).loop_load_page("//*[contains(text(), 'Яндекс')]")

    def start_job_search_target_site(self):

        print(f'{self.msg} Открываю yandex')

        res_load = LoadPage(self.driver, self.url, self.dir_project).loop_load_page("//*[contains(text(), 'Яндекс')]")

        if not res_load:
            return False

        time.sleep(2)

        res_modal = YandexCheckModal(self.driver).start_check_modal()

        if not self.write_request():
            return False

        res_search_site = YandexLoopPage(self.driver, self.target_request, self.dir_project,
                                         self.google_alternate, self.name_profile).start_loop_page()

        return res_search_site
