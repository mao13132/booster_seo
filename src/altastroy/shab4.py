import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from src.yandex.scroll import Scroll


class Shab4:
    def __init__(self, driver):

        self.driver = driver

        self.scroll_core = Scroll(driver)

        self.list_time = [187, 235, 278, 194, 261]

        self.micro_sleep = [19, 24, 16, 13, 31]

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

    def click_logo(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на логотип')

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

    def click_cabinet(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на вход в кабинет')

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[@class='block-login']").click()

        except:
            return False

        return True

    def click_phone_form(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на обратный звонок')

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

    def click_buy(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на купить')

        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"//*[contains(text(), 'Купить')]")[1].click()
        except:

            try:
                self.driver.find_elements(by=By.XPATH,
                                          value=f"//*[contains(text(), 'Купить')]")[2].click()
            except:
                return False

        time.sleep(2)

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Продолжить покупки')]").click()
        except:
            pass

        return True

    def start_shab(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Зашёл на целевой сайт. Начинаю имитацию поведения человека по шаблону 4')

        self.click_buy()

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        _mic = random.choice(self.micro_sleep)

        self.scroll_core.set_scroll_range(_mic)

        self.click_cabinet()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: кликаю на логотип')

        click_logo = self.click_logo()

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

        self.click_phone_form()

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Закончил обработку целевого сайта')

        return True
