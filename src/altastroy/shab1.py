import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from src.yandex.scroll import Scroll


class Shab1:
    def __init__(self, driver):

        self.driver = driver

        self.scroll_core = Scroll(driver)

        self.list_time = [183, 212, 231, 198, 201]

        self.micro_sleep = [15, 25, 10, 5, 30]

    def click_review(self, value):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на "{value}"')

        try:
            list_buttons = self.driver.find_elements(by=By.XPATH,
                                                     value=f"//*[contains(text(), '{value}')]")
        except:
            return False

        try:
            list_buttons[-1].click()
        except:
            return False

        return True

    def start_shab(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Зашёл на целевой сайт. Начинаю имитацию поведения человека по шаблону 1')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(5)

        _sec = random.choice(self.micro_sleep)

        time.sleep(_sec)

        self.click_review('Отзывы')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(5)

        _sec = random.choice(self.micro_sleep)

        time.sleep(_sec)

        self.click_review('Акции')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(10)

        _sec = random.choice(self.micro_sleep)

        time.sleep(_sec)

        self.click_review('Магазины')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(8)

        _sec = random.choice(self.micro_sleep)

        time.sleep(_sec)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Закончил обработку целевого сайта')

        return True
