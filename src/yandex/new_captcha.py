import asyncio
import os
import random
import time

from twocaptcha import TwoCaptcha

from settings import CAPTCHA_TOKEN
from src.yandex.stoper import Stoper

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


class NewCaptcha:
    def __init__(self, driver, dir_project):
        self.driver = driver
        self.count_tile_wait = [0.1, 0.2, 1.3]

        self.count_try = 3

        self.dir_project = dir_project

    def _check_url_capt(self):
        self._captcha_url = self.driver.current_url

        if 'captcha' in self._captcha_url:
            return True

        return False

    def _check_click(self):
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

    def check_good_click(self):
        count = 0

        count_wait_load = 15

        while True:
            count += 1
            if count > count_wait_load:
                print(f'Не загрузилась каптча после начального клика на неё')
                return False

            try:
                elem = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'AdvancedCaptcha-View')]")
            except:
                time.sleep(1)
                continue

            return True

    def one_step_click(self):
        if self._check_click():

            # Кликаю по запуску для генерации каптчи если требуется
            if not self.click_captcha_one_windows():
                return False

            res_load = self.check_good_click()

            return res_load

    def get_image_captcha(self):
        try:
            link_img_captcha = self.driver.find_element(by=By.XPATH,
                                                        value=f"//*[contains(@class, 'ImageWrapper')]/img")
        except:
            return False

        return link_img_captcha.screenshot_as_base64

    def get_image_two_job(self):
        try:
            link_img_captcha = self.driver.find_element(by=By.XPATH,
                                                        value=f"//*[contains(@class, 'SilhouetteTask')]/img")
        except:
            return False

        name = os.path.join(self.dir_project, 'src', 'captcha', 'captcha.jpg')

        with open(name, "wb") as elem_file:
            elem_file.write(link_img_captcha.screenshot_as_png)

        return name

    def _job_captcha(self, one_image, two_image):

        try:

            api_rucaptcha = self.solver.coordinates(one_image, hintImg=two_image,
                                                    hintText="Кликните в таком порядке | "
                                                             "Click in the following order", lang='ru')

        except Exception as es:
            print(f'Ошибка при формирование капчи "{es}"')
            return False

        if api_rucaptcha['code'] != '':
            print(f'Разгадал карчу "{api_rucaptcha["code"]}"')

            x = 0

            y = 0

            test = self.driver.find_element(by=By.XPATH,
                                            value=f"//*[contains(@class, 'ImageWrapper')]/img")

            ActionChains(self.driver).move_to_element(test).move_by_offset(-150 + x, -80 + y).click().perform()

    def new_captcha(self):
        self.solver = TwoCaptcha(CAPTCHA_TOKEN)

        image_link = self.get_image_captcha()

        image_two_job = self.get_image_two_job()

        res_captcha = self._job_captcha(image_link, image_two_job)

        print()

    def check_captcha(self):
        """Возвращаю Tru если можно идти дальше коду"""

        if not self._check_url_capt():
            return False

        print(f'Обнаружена каптча при сканирование строчек в yandex')

        res_load_captcha = self.one_step_click()

        if not res_load_captcha:
            return False

        res_captcha = self.new_captcha()

        check_job_captcha = self._check_url_capt()

        return check_job_captcha
