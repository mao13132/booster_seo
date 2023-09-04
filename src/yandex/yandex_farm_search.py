import asyncio
import random
from datetime import datetime
from time import perf_counter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.yandex.captcha_core import CoreCaptcha
from src.yandex.load_page import LoadPage
from src.yandex.stoper import Stoper
from src.yandex.yandex_insert_request import YandexInsertRequest


class YandexFarmSearch:
    def __init__(self, driver, name_profile, target_request):
        self.driver = driver
        self.msg = f'Аккаунт: "{name_profile}"'
        self.site = 'https://altastroy-nn.ru'

        self.target_request = target_request



    def start_job_search_target_site(self):
        url = 'https://yandex.ru/search'

        res_load_page = LoadPage(self.driver, url).loop_load_page(
            "//*[contains(text(), 'Яндекс')]")

        res_insert_request = YandexInsertRequest(self.driver).check_insert_search(self.target_request)

        print()
