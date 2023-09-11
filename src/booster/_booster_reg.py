import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.yandex.load_page import LoadPage
from src.yandex.sms_activate_api import SmsActivateApi


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
                print(f'BoosterSeo: Возможно спутана учетка старая и туда регаю новую')
                self.driver.find_elements(by=By.XPATH,
                                          value=f"//*[contains(@href, 'passport.yandex.ru/registration')]")[-1].click()

                time.sleep(2)

                self.driver.find_element(by=By.XPATH,
                                         value=f"//*[contains(text(), 'я себя')]").click()

                return True

            except Exception as es:
                print(f'BoosterSeo: Ошибка при клике на кнопку ВОЙТИ {es}')
                return False

    def check_load_page_register(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(@for, "phone")]')))
            return True
        except:
            print(f'BoosterSeo: Ошибка при загрузке страницы регистрации')
            return False

    def insert_name(self):

        for simbol in self.data_user['name_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[@name="firstname"]').send_keys(simbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: Ошибка при написание имени при регистрации {es}')
                return False

        return True

    def insert_surname(self):
        for symbol in self.data_user['surname_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[@name="lastname"]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание фамилии при регистрации {es}')
                return False

        return True

    def insert_password(self):
        for symbol in self.data_user['password_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//input[@id="password"]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание пароля при регистрации {es}')
                return False

        return True

    def insert_two_password(self):
        for symbol in self.data_user['password_account']:

            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f'//*[contains(@data-t, "input-password_confirm")]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание 2 пароля при регистрации {es}')
                return False

        return True

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

        if not self.insert_two_password():
            return False

        time.sleep(random.choices(self._count_tile_wait)[0])

        return True

    def click_login(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f'//*[contains(@class, "login")]//*[contains(text(), "огин")]').click()
        except:
            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f'//*[contains(@class, "form")]//*[contains(text(), "огин")]').click()
            except Exception as es:
                print(f'BoosterSeo: ошибка при клике на логин {es}')
                return False

        time.sleep(3)

        try:

            list_login = self.driver.find_elements(by=By.XPATH,
                                                   value=f'//*[contains(@class, "list")]//*[contains(@class, "option")]')
        except:
            # print(f'BoosterSeo: Не смог получить список логинов')
            pass
        try:
            _count_click_login = random.randint(1, 3)

            list_login[_count_click_login].click()

            time.sleep(5)
        except:

            try:
                ses = self.driver.find_elements(by=By.XPATH,
                                                value=f'//*[contains(@class, "reg-field")]'
                                                      f'//*[contains(@class, "registration")]')

                count = random.randint(0, len(ses))

                ses[count].click()

            except:
                # print(f'BoosterSeo: yandex не предложил логинов')

                return False

        return True

    def insert_generation_login(self):

        for symbol in self.data_user['login_account']:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//input[@id="login"]').send_keys(symbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание сгенерированного логина {es}')
                return False

        return True

    def get_save_login(self):
        try:

            login_account = self.driver.find_element(by=By.XPATH, value=f'//input[@id="login"]').get_attribute('value')

            print(f'BoosterSeo: логин: {login_account}')

        except:
            print(f'BoosterSeo: Ошибка при получение данных о логине')
            return False

        return login_account

    def write_phone(self, phone):

        print(f'BoosterSeo: Входящий номер {phone}')

        try:

            self.driver.find_element(by=By.XPATH, value=f'//*[contains(text(), "омер моб")]').click()

        except:
            pass

        time.sleep(1)

        for simbol in phone[1:]:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//*[@name="phone"]').send_keys(simbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание номера телефона {es}')
                return False

        return True

    def _check_write_phone(self):
        try:
            self._value_phone = self.driver.find_element(by=By.XPATH, value=f'//*[@name="phone"]').get_attribute(
                "value")

        except:
            return False

        if self.number_phone[1:] in self._value_phone:
            return True

        return False

    def clicker_send_sms_button(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f'//*[contains(text(), "Подтвер")]//parent::button').click()

            return True

        except:
            pass

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f'//*[contains(text(), "Получить код")]//parent::button').click()

            return True

        except:
            pass

        return False

    def loop_write_sms(self):

        _count = 0

        while True:
            _count += 1

            if _count == 31:
                print(f'BoosterSeo: Не дождался смс - отправил отмену номера. Сбрасываю попытку')
                return False

            status = self.smscore.get_status(self.number_id)

            if 'STATUS_OK' in status:
                _status_out = str(status).split(':')[-1]
                _status_out = _status_out.replace('-', '')
                return _status_out

            print(f'BoosterSeo: #{_count} попытка получения смс')

            time.sleep(5)

    def _check_load_aprove_registratin(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//*[contains(@data-t, "registration")]//button[contains(@class, action)]')))
            return True
        except:
            print(f'BoosterSeo: Ошибка при загрузке страницы с кнопкой "зарегистрироваться"')
            return False

    def click_over_registration_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f'//*[contains(@data-t, "registration")]//button[contains(@class, action)]').click()
        except:
            print(f'BoosterSeo: Ошибка при клики на кнопку "Зарегестрироваться"')
            return False

        return True

    def _check_over_load_page(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "аккаунт готов")]')))
            return True
        except:
            print(f'BoosterSeo: Ошибка при загрузке последней страницы регистрации')
            return False

    def click_propustit(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f'//a[contains(@href, "https://sso.passport.yandex.ru/prepare")]').click()
        except:
            return False

        return True

    def write_sms_code(self, code):

        for simbol in code:

            try:
                self.driver.find_element(by=By.XPATH, value=f'//input[contains(@name, "phoneCode")]').send_keys(simbol)

                time.sleep(random.choices(self._count_tile_wait)[0])

            except Exception as es:
                print(f'BoosterSeo: ошибка при написание sms ответ {es}')
                return False

        return True

    def write_data_to_google_sheet(self, last_good_row):

        _data = [self.data_user['name_profile'], self.data_user['user_agent'], 0, 0,
                 f"{self.data_user['login_account']};{self.data_user['password_account']}",
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        res_write = self.google_alternate.write_in_range_account('аккаунты', last_good_row, _data)

        return res_write

    def loop_set_login(self):

        count = 0

        count_try = 5

        while True:

            count += 1

            if count > count_try:
                print(f'Не смог получить логин')

                return False

            res_click = self.click_login()

            if not res_click:
                # print(f'BoosterSeo: Не подтверждаю выбор логина, генерирую свой')
                self.insert_generation_login()

            _login = self.get_save_login()

            if _login == '':
                time.sleep(2)
                continue

            return _login

    def start_reg(self, last_good_row):

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

        print(f'BoosterSeo: вписываю данные аккаунта')

        res_insert = self.insert_data_account_to_form()

        if not res_insert:
            return False

        self.data_user['login_account'] = self.loop_set_login()

        self.smscore = SmsActivateApi()

        phone = self.smscore.get_number('ya', 'any')

        if not phone:
            return False

        self.number_phone = phone['phoneNumber']

        self.number_id = phone['activationId']

        self.response_write_phone = self.write_phone(self.number_phone)

        if not self.response_write_phone:
            print(f'BoosterSeo: Не смог написать номер - Отменяю смс')
            self.smscore.set_status(self.number_id, 8)
            return False

        if not self._check_write_phone():
            print(f'BoosterSeo: Не могу подтвердить написание номера')
            self.smscore.set_status(self.number_id, 8)
            return False

        if not self.clicker_send_sms_button():
            print(f'BoosterSeo: Не смог нажать на кнопку отправить смс')
            self.smscore.set_status(self.number_id, 8)
            return False

        print(f'BoosterSeo: Отправляю запрос о том что смс была отправлена')

        self.smscore.set_status(self.number_id, 1)

        response_sms_code = self.loop_write_sms()

        if not response_sms_code:
            self.smscore.set_status(self.number_id, 8)
            return False

        print(f'BoosterSeo: Получил смс {response_sms_code}')

        if not self.write_sms_code(response_sms_code):
            print(f'BoosterSeo: Не смог написать смс ответ регистрации yandex')
            return False

        time.sleep(1)

        if not self._check_load_aprove_registratin():
            return False

        if not self.click_over_registration_button():
            return False

        if not self._check_over_load_page():
            return False

        self.click_propustit()

        self.smscore.set_status(self.number_id, 6)

        self.write_data_to_google_sheet(last_good_row)

        print(f'BoosterSeo: Успешно зарегистрировал аккаунт {self.data_user["name_profile"]}')

        return True
