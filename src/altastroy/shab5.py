import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from src.yandex.scroll import Scroll


class Shab5:
    def __init__(self, driver):

        self.driver = driver

        self.scroll_core = Scroll(driver)

        self.list_time = [211, 187, 147, 258, 247]

        self.micro_sleep = [33, 15, 17, 21, 44]

        self.links = ['Душевые кабины', 'Раковины', 'Биде', 'Водонагреватели']

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
              f'BoosterSeo: Зашёл на целевой сайт. Начинаю имитацию поведения человека по шаблону 5')

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        self.close_pop_up()

        _link = random.choice(self.links)

        self.click_review(_link)

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        self.click_buy()

        _sec = random.choice(self.list_time)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Засыпаю на {_sec} секунд(у)')

        time.sleep(_sec)

        _mic = random.choice(self.micro_sleep)

        self.scroll_core.set_scroll_range(_mic)

        _mic = random.choice(self.micro_sleep)

        time.sleep(_mic)

        _link = random.choice(self.links)

        self.click_review(_link)

        self.click_buy()

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
