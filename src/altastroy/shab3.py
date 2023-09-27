import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from settings import NAME_SERVER
from src.yandex.scroll import Scroll


class Shab3:
    def __init__(self, driver):

        self.driver = driver

        self.scroll_core = Scroll(driver)

        self.list_time = [169, 224, 261, 197, 216]

        self.micro_sleep = [18, 28, 17, 7, 35]

        self.links = ['Отзывы', 'Акции', 'Магазины']

    def click_review(self, value):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: кликаю на "{value}"')

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

    def click_logo(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: кликаю на логотип')

        try:
            list_buttons = self.driver.find_elements(by=By.XPATH,
                                                     value=f"//*[contains(@class, 'logo')]")
        except:
            return False

        try:
            list_buttons[-1].click()
        except:
            return False

        return True

    def click_phone_form(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: кликаю на обратный звонок')

        try:
            list_buttons = self.driver.find_elements(by=By.XPATH,
                                                     value=f"//*[contains(@class, 'block-phone-form')]")
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
              f'{NAME_SERVER} Booster Seo: Зашёл на целевой сайт. Начинаю имитацию поведения человека по шаблону 3')

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        _mic = random.choice(self.micro_sleep)

        self.scroll_core.set_scroll_range(_mic)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: кликаю на логотип')

        click_logo = self.click_logo()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.close_pop_up()

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.click_phone_form()

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Закончил обработку целевого сайта')

        return True
