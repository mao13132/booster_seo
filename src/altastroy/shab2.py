import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from src.yandex.scroll import Scroll


class Shab2:
    def __init__(self, driver):

        self.driver = driver

        self.scroll_core = Scroll(driver)

        self.list_time = [172, 214, 257, 191, 214]

        self.micro_sleep = [17, 27, 12, 3, 28]

        self.links = ['Отзывы', 'Акции', 'Магазины']

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

    def close_pop_up(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'popup__main')]"
                                           f"//button[contains(@class, 'close')]").click()
        except:
            return False

        return True

    def start_shab(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Зашёл на целевой сайт. Начинаю имитацию поведения человека по шаблону 2')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        _mic = random.choice(self.micro_sleep)

        self.scroll_core.set_scroll_range(_mic)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        self.close_pop_up()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Закончил обработку целевого сайта')

        return True
