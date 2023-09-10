import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.yandex.load_page import LoadPage


class _BoosterReg:
    def __init__(self, google_alternate, dir_project, android_phone, driver, data_user):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone
        self.driver = driver
        self.data_user = data_user

        self._count_tile_wait = [0.1, 0.2, 1.3]

    def click_register_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@href, 'passport.yandex.ru/registration')]").click()
            return True
        except:
            try:
                print(f'Возможно спутана учетка старая и туда регаю новую')
                self.driver.find_elements(by=By.XPATH,
                                          value=f"//*[contains(@href, 'passport.yandex.ru/registration')]")[-1].click()

                time.sleep(2)

                self.driver.find_element(by=By.XPATH,
                                         value=f"//*[contains(text(), 'я себя')]").click()

                return True

            except Exception as es:
                print(f'Ошибка при клике на кнопку ВОЙТИ {es}')
                return False

    def check_load_page_register(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(@for, "phone")]')))
            return True
        except:
            print(f'Ошибка при загрузке страницы регистрации')
            return False

    def insert_name(self):

        for simbol in self.data_user['name_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[@name="firstname"]').send_keys(simbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'Ошибка при написание имени при регистрации {es}')
                return False

        return True

    def insert_surname(self):
        for symbol in self.data_user['surname_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[@name="lastname"]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'ошибка при написание фамилии при регистрации {es}')
                return False

        return True

    def insert_password(self):
        for symbol in self.data_user['password_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//input[@id="password"]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'ошибка при написание пароля при регистрации {es}')
                return False

    def insert_data_account_to_form(self):
        if not self.insert_name():
            return False
        time.sleep(random.choices(self._count_tile_wait)[0])

        if not self.insert_surname():
            return False
        time.sleep(random.choices(self._count_tile_wait)[0])

        if not self.insert_password():
            return False
        time.sleep(random.choices(self._count_tile_wait)[0])

    def click_login(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f'//*[contains(@class, "login")]//*[contains(text(), "огин")]').click()
        except:
            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f'//*[contains(@class, "form")]//*[contains(text(), "огин")]').click()
            except Exception as es:
                print(f'ошибка при клике на логин {es}')
                return False

        time.sleep(3)

        try:

            list_login = self.driver.find_elements(by=By.XPATH,
                                                   value=f'//*[contains(@class, "list")]//*[contains(@class, "option")]')
        except:
            print(f'Не смог получить список логинов')

        try:
            self._count_click_login = random.randint(1, 3)

            list_login[self._count_click_login].click()

            time.sleep(5)
        except:

            try:
                ses = self.driver.find_elements(by=By.XPATH,
                                                value=f'//*[contains(@class, "reg-field")]'
                                                      f'//*[contains(@class, "registration")]')

                count = random.randint(0, len(ses))

                ses[count].click()

            except:
                print(f'Ошибка при клике на логин')

        return True

    def insert_generation_login(self):

        for symbol in self.data_user['login_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[contains(@class, "login")]'
                                                            f'//*[contains(@name, "login")]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'ошибка при написание сгенерированного логина {es}')
                return False

        return True

    def get_save_login(self):
        try:
            login_account = self.driver.find_element(by=By.XPATH, value=f'//*[contains(@class, '
                                                                             f'"login")]//*[@id="login"]')\
                .get_attribute("value")

            print(f'логин: {login_account}')
        except:
            print(f'Ошибка при получение данных о логине')
            return False

        return login_account

    def start_reg(self):
        url = 'https://mail.yandex.ru'

        res_load = LoadPage(self.driver, url, self.dir_project).loop_load_page("//*[contains(text(), 'Яндекс')]")

        if not res_load:
            return False

        res_click_reg = self.click_register_button()

        if not res_click_reg:
            return False

        res_load_reg = self.check_load_page_register()

        if not res_load_reg:
            return False

        res_insert = self.insert_data_account_to_form()

        if not res_insert:
            return False

        res_click = self.click_login()

        # TODO если логин яндекс даёт то надо достать его

        if not res_click:
            print(f'Не подтверждаю выбор логин генерирую свой')
            self.insert_generation_login()

        good_login = self.get_save_login()

        self.smscore = SmsActivateApi()

        self.phone = self.get_phone()

        if not self.phone:
            return False

        print()
