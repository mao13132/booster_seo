import asyncio
import random

from twocaptcha import TwoCaptcha

from src.yandex.stoper import Stoper

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

class CoreCaptcha:
    def __init__(self, driver):
        self.driver = driver
        self._coun_tile_wait = [0.1, 0.2, 1.3]

    def __check_url_capt(self):
        self._captcha_url = self.driver.current_url

        if 'captcha' in self._captcha_url:
            self.task['captcha'] = True
            return True

        return False

    def check_captha(self):
        """Возращаю Tru если можно идти дальше коду"""

        if not self.__check_url_capt():
            # Если проверка говорит что нет капчм возращаю True как знак что можно идти дальше

            self.task['dict'][f'captcha'] = True

            return True

        print(f'Обнаружена капча при сканирование строчек в yandex')

        self._counter_captcha = 0
        while True:

            if self._counter_captcha == 3:
                # Не смог разгадать 3 раза
                return False

            self.response_mid_captcha = self.mid_captcha()
            # self.response_mid_captcha = self.mid_captcha()

            if not self.__check_url_capt():
                # Если проверка говорит что нет капчм возращаю True как знак что можно идти дальше
                return True

            self._counter_captcha += 1

    def _check_text_image(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//form[@method='POST']//*[contains(text(), 'текст с кар')]")))

            print(f'Увидел картинку с капчой иду решать')
            return True
        except:
            # print(f'Не вижу страницы с введитекс с капчи')
            return False

    def __check_click(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//form[@method='POST']//*[contains(@class, 'CheckboxCaptcha-Anchor')]")))

            print(f'Вижу кнопку на капче - иду жать')
            return True
        except:
            print(f'Не вижу кнопки на которую надо нажать - игнорю')
            return False

    def click_captcha_one_windows(self):
        try:

            self.driver.find_element(by=By.XPATH,
                                     value=f"//form[@method='POST']//*[contains(@class, 'CheckboxCaptcha-Anchor')]").click()
            return True

        except:
            print(f'Не смог нажать кнопку на капче')

        return False

    def mid_captcha(self):

        self.solver = TwoCaptcha('faf8570118f0d701a126122a102036ec')

        if self.__check_click():
            if not self.click_captcha_one_windows():
                return False

        if not self._check_text_image():
            return True

        self.counter = 0
        while True:

            if self.counter >= 12:
                return False

            try:
                self.link_img_captcha = self.driver.find_element(by=By.XPATH,
                                                                 value=f"//*[contains(@class, 'AdvancedCaptcha-View')]"
                                                                       f"//img[contains(@src, "
                                                                       f"'https://yandex.ru/"
                                                                       f"captchaimg?')]").get_attribute("src")
            except Exception as es:
                print(f'Не смог получить ссылку с картинкой на капчу {es}')

            try:
                self.api_rucaptcha = self.solver.normal(self.link_img_captcha)

            except Exception as es:
                print(f'Не смог отправить в ручапчу капчу {es}')

            try:
                if self.api_rucaptcha['code'] != '':

                    print(f'Разгадал карчу "{self.api_rucaptcha["code"]}"')

                    try:
                        self.captcha_input = self.driver.find_element(by=By.XPATH,
                                                                      value=f"//*[contains(@class, 'AdvancedCaptcha')]"
                                                                            f"//*[contains(@name, "
                                                                            f"'rep')]")

                        for simbol in self.api_rucaptcha['code']:

                            try:
                                self.captcha_input.send_keys(simbol)
                                asyncio.run(Stoper().stoper(random.choices(self._coun_tile_wait)[0]))

                            except Exception as es:
                                print(f'ошибка при написание капчи {es}')

                                return False

                        try:
                            self.driver.find_elements(by=By.XPATH,
                                                      value=f"//*[contains(@class, 'AdvancedCaptcha')]"
                                                            f"//button")[-1].click()
                        except:
                            print(f'Ошибка при клике на проверку написаной капчи')

                        # TODO удачное разгадывание

                        return True


                    except Exception as es:
                        print(f'ошибка при печатания капчи {es}')

            except:

                asyncio.run(Stoper().stoper(5))

                self.counter += 1

            asyncio.run(Stoper().stoper(5))

            self.counter += 1
