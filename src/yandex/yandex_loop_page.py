import asyncio
import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from settings import MAX_COUNT_PAGE
from src.yandex.new_captcha import NewCaptcha
from src.yandex.scroll import Scroll
from src.yandex.stoper import Stoper


class YandexLoopPage:
    def __init__(self, driver, target_request, dir_project, google_alternate, name_profile, _request):

        self.driver = driver

        self.site = 'altastroy-nn.ru'

        self.count_try = 3

        self.target_request = target_request

        self.scroll_core = Scroll(driver)

        self.time_lists = [1.1, 1.2, 1.3, 0.9]

        self.dir_project = dir_project

        self.captcha_core = NewCaptcha(self.driver, dir_project)

        self.google_alternate = google_alternate

        self.name_profile = name_profile

        self._request = _request

    def get_rows(self):

        count = 0

        while True:

            count += 1

            if count > self.count_try:
                print(f'Не смог получить строчки с поисковой страницы yandex')
                return False

            try:
                rows_yandex = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'serp-item')]")
            except:
                time.sleep(1)
                continue

            if rows_yandex == []:
                self.captcha_core.check_captcha()
                time.sleep(1)
                continue

            return rows_yandex

    def scroll_one_page_search(self, count, count_page_):

        if count_page_ > 2:
            count -= 1

        if count > 10:
            count = 10

        _count = 0

        while True:

            # if self._count % 10 == 0:
            # print(f'Клик на редромную ссылку кроме noclick')
            # self.click_random_link()

            list_time_stop = ['91', '93', '95', '97', '101', '103', '105', '107']

            _count += 1

            take_value_scroll = random.choices(list_time_stop)[0]

            self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {take_value_scroll})")
            asyncio.run(Stoper().stoper(0.2))
            self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {take_value_scroll})")

            self.list_time = [0.9, 1.2, 1.6, 2.1, 1.8, 1.4]

            asyncio.run(Stoper().stoper(random.choices(self.list_time)[0]))

            if _count > count:
                return True

    def open_target_site(self, value):
        elements = value.find_elements(by=By.XPATH, value=f".//a[contains(@class, 'Link')]")

        if elements == []:
            return False

        for el in elements:
            try:
                el.click()

                return True

            except:
                continue

        return False

    def write_new_value_sheet(self, count_page_, count_row_):
        row_ = self._request['row'] + 2

        columns_ = 4

        res_write = self.google_alternate.write_in_cell(self._request['name_sheet'], row_, columns_, count_page_)

        time.sleep(1)

        columns_ = 5

        res_write = self.google_alternate.write_in_cell(self._request['name_sheet'], row_, columns_, count_row_)

        return res_write

    def loop_rows(self, list_rows, count_page_):

        """Здесь идёт проверка всех строчек на целевой сайт и слово РЕКЛАМА"""

        for count, value in enumerate(list_rows):

            count_row_ = count + 1

            try:
                link = value.find_element(by=By.XPATH, value=f".//a").get_attribute('href')
            except:
                continue

            if self.site in link:

                if 'еклама' in value.text:
                    continue

                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'BoosterSeo: Найден целевой сайт по запросу: "{self.target_request}" на {count_page_} '
                      f'страницы и {count_row_} строке')

                res_write = self.write_new_value_sheet(count_page_, count_row_)

                res_open = self.open_target_site(value)

                if res_open:
                    return True

        return False

    def paginator(self, page_count):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//a[contains(text(), 'дальше')]").click()
            return True
        except:
            self.scroll_core.scroll_mikro()
            pass

        try:
            self._rows_page = self.driver.find_elements(by=By.XPATH,
                                                        value="//*[@class='pager']//a")

            if page_count < 3:
                self._rows_page[page_count - 1].click()
                return True
            else:
                self._rows_page[2].click()
                return True
        except:
            self.scroll_core.scroll_mikro()
            pass

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Показать ещё')]//parent::button").click()

            return True
        except:
            pass

        # print(f'Не должно до сюда доходить')

        print(f' Кончились страницы или до должен доходить сюда. Фильры с верху не работают?')
        return False

    def action_no_search_site(self, count_scroll, count_page_):
        self.scroll_one_page_search(count_scroll, count_page_)

        return True

    def loop_page_farm_yandex(self):
        for count_page in range(MAX_COUNT_PAGE):

            if self.captcha_core.check_captcha():
                continue

            count_page_ = count_page + 1

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'Ищу сайт "{self.site}" на {count_page_} странице yandex')

            # Получаю строки
            list_rows = self.get_rows()

            if not list_rows or list_rows == []:
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'Не смог получить поисковые строчки. Проверьте user agent "{self.name_profile}"')
                return False

            # Цикл где каждую строчку проверяю на целевой сайт и рекламу
            job_link = self.loop_rows(list_rows, count_page_)

            # TODO перенести. Здесь при обнаружение целевого сайта создаю запись в словаре

            if job_link:
                return job_link

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'BoosterSeo: Целевой сайт на странице {count_page_} не обнаружен')

            # Вычисляю сколько мне надо крутить в низ страницу
            count_scroll = len(list_rows) // 2

            # Пролистываю страницу
            res_no_search = self.action_no_search_site(count_scroll, count_page_)

            if self.captcha_core.check_captcha():
                continue

            # Переключатель страниц
            res_paginator = self.paginator(count_page_)

            if not res_paginator:
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'закончились страницы. Не смог переключить страницу, возможно такой вид дизайна')
                return False

            asyncio.run(Stoper().stoper(random.choices(self.time_lists)[0]))

        print(f'Все страницы обошёл')

        return False

    def tab_switch(self):

        self.driver.close()

        try:
            # TODO при US 2 вкладка, если другой браузер смотреть дополнительно
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except Exception as es:
                print(f'Ошибка при переключение второго окна "{es}"')
                return False

            return True

        except Exception as es:
            print(f'Исключение при работе с 2м окном {es}')
            return False

    def start_loop_page(self):
        res_loop = self.loop_page_farm_yandex()

        if res_loop:
            self.tab_switch()

            return True

        return res_loop
