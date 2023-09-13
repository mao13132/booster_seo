import asyncio
import base64
import os
import random
import time
from datetime import datetime

import PIL.Image
import requests
from PIL import Image
import math

from twocaptcha import TwoCaptcha

from settings import CAPTCHA_TOKEN
from src.telegram_debug import SendlerOneCreate
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
        try:
            self._captcha_url = self.driver.current_url
        except Exception as es:
            print(f"Ошибка при заборе адресной строки. Капча '{es}'")
            return False

        if 'captcha' in self._captcha_url:
            return True

        return False

    def _check_click(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//form[@method='POST']//*[contains(@class, 'CheckboxCaptcha-Anchor')]")))

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: Обнаружена капча')
            return True
        except:
            return False

    def click_captcha_one_windows(self):
        try:

            self.driver.find_element(by=By.XPATH,
                                     value=f"//form[@method='POST']//*[contains(@class, 'CheckboxCaptcha-Anchor')]").click()
            return True

        except:

            return False

    def check_good_click(self):
        count = 0

        count_wait_load = 15

        while True:
            count += 1
            if count > count_wait_load:
                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: Не загрузилась каптча после начального клика на неё')
                return False

            try:
                elem = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'AdvancedCaptcha-View')]")
            except:
                time.sleep(1)

                if not self._check_url_capt():
                    return False

                continue

            return True

    def one_step_click(self):
        if self._check_click():
            # Кликаю по запуску для генерации каптчи если требуется
            self.click_captcha_one_windows()

            res_load = self.check_good_click()

            return res_load

        else:
            return True

    def resize_image(self, name_file):
        try:
            foo = Image.open(name_file)
            foo = foo.convert('RGB')
            x, y = foo.size
            x2, y2 = math.floor(x - 1), math.floor(y - 1)
            foo = foo.resize((x2, y2), PIL.Image.LANCZOS)
            foo.save(name_file, quality=95)
        except Exception as es:

            SendlerOneCreate('').save_text(f'Ошибка при конвертирование капчи "{es}"')

            return False

        return name_file

    def crop_image(self, name_file):
        try:
            foo = Image.open(name_file)
            foo = foo.convert('RGB')
            foo = foo.crop((0, 0, 100, 20))
            foo.save(name_file)

        except Exception as es:

            SendlerOneCreate('').save_text(f'Ошибка при crop_image капчи "{es}"')

            return False

        return name_file

    def load_image_to_base64(self, name_file):

        with open(name_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

            encoded_string = encoded_string.decode('utf-8')

        return encoded_string

    def save_image_elem(self, elem, name):

        name_ = os.path.join(self.dir_project, 'src', 'captcha', f'{name}.jpg')

        with open(name_, "wb") as elem_file:
            elem_file.write(elem.screenshot_as_png)

        return name_

    def _get_image_captcha(self, xpatch):
        try:
            link_img_captcha = self.driver.find_element(by=By.XPATH,
                                                        value=f"//*[contains(@class, '{xpatch}')]/img")
        except:
            return False

        return link_img_captcha

    def get_image_captcha(self):

        elem = self._get_image_captcha('ImageWrapper')

        name_image_two_job = self.save_image_elem(elem, 'image_captcha')

        name_image_two_job = self.resize_image(name_image_two_job)

        file_base64 = self.load_image_to_base64(name_image_two_job)

        return file_base64

    def get_image_two_job(self):

        elem = self._get_image_captcha('SilhouetteTask')

        name_image_two_job = self.save_image_elem(elem, 'image_two_job')

        name_image_two_job = self.crop_image(name_image_two_job)

        file_base64 = self.load_image_to_base64(name_image_two_job)

        return file_base64

    def loop_check_good_code(self, code):

        for _try in range(30):

            resul = requests.get(f'http://rucaptcha.com/res.php?key={CAPTCHA_TOKEN}&action=get&id={code}&json=1')

            if resul.status_code != 200:
                time.sleep(1)
                continue

            result = resul.json()

            if result['request'] == 'CAPCHA_NOT_READY':
                time.sleep(5)
                continue

            return result['request']

        SendlerOneCreate('').save_text(f'Ошибка при получение ответ от капчи ')

        return False

    def send_captcha(self, one_image, two_image):

        data_ = {
            'method': 'base64',
            'coordinatescaptcha': '1',
            'key': CAPTCHA_TOKEN,
            'body': one_image,
            'imginstructions': two_image
        }

        for _try in range(3):
            resul = requests.post('http://rucaptcha.com/in.php', data=data_)

            if resul.status_code != 200:
                continue

            good_response = resul.text

            if 'OK' not in good_response:
                continue

            status_code = good_response.replace('OK|', '')

            coordinate_captcha = self.loop_check_good_code(status_code)

            return coordinate_captcha

        print(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: Исчерпал все попытки на получения ответа по капче')

        return False

    def loop_set_coordinate(self, dict_):

        for coor_ in dict_:
            x = int(coor_["x"])
            y = int(coor_["y"])

            try:
                test = self.driver.find_element(by=By.XPATH,
                                                value=f"//*[contains(@class, 'ImageWrapper')]/img")
                ActionChains(self.driver).move_to_element(test).move_by_offset(-150 + x, -80 + y).click().perform()
            except Exception as es:
                print(f'Ошибка "{es}"')

                continue

            time.sleep(3)

        return True

    def click_send_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'SubmitContent')]").click()
        except:
            return False

        return True

    def new_captcha(self):

        try:
            self.solver = TwoCaptcha(CAPTCHA_TOKEN)
        except Exception as es:

            SendlerOneCreate('').save_text(f'Captcha Checker: Ошибка при подключение "{es}"')

            return False

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: распознаю изображение')

        image_link = self.get_image_captcha()

        image_two_job = self.get_image_two_job()

        res_captcha = self.send_captcha(image_link, image_two_job)

        if not res_captcha:
            return False

        res_set_ = self.loop_set_coordinate(res_captcha)

        if not res_set_:
            return False

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: изображение распознано')

        res_click_button = self.click_send_button()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Captcha Checker: отправляю на проверку')

        return res_click_button

    def loop_check_captcha(self):

        for _try in range(5):

            if _try > 0:

                check_job_captcha = self._check_url_capt()

                if not check_job_captcha:
                    return True

                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'Captcha Checker: повторная попытка решения капчи')

            res_load_captcha = self.one_step_click()

            if not res_load_captcha:
                self.driver.refresh()
                time.sleep(1)
                continue

            res_captcha = self.new_captcha()

            if not res_captcha:
                self.driver.refresh()
                time.sleep(1)
                continue

        SendlerOneCreate('').save_text(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                                       f'Captcha Checker: Все попытки по получению капчи исчерпаны')

        return False

    def check_captcha(self):
        """Возвращаю Tru если можно идти дальше коду"""

        if not self._check_url_capt():
            return False

        check_loop_captcha = self.loop_check_captcha()

        return check_loop_captcha
