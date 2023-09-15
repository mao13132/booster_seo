from datetime import datetime

from settings import NAME_SERVER, MAX_CLICK_ONE_ACCOUNT
from src.altastroy.choice_shab import CoiceShab

from src.browser.createbrowser import CreatBrowser
from src.google.google_core import ConnectGoogleCore

from src.telegram_debug import SendlerOneCreate

from src.yandex.yandex_start_search import YandexFarmSearch


class IterJob:
    def __init__(self, google_alternate, list_requests, list_profile, dir_project, android_phone):

        self.google_alternate = google_alternate

        self.list_requests = list_requests

        self.list_profile = list_profile

        self.dir_project = dir_project

        self.android_phone = android_phone

    def start_profile(self, name_profile, user_agent):

        try:

            browser = CreatBrowser(self.dir_project, name_profile, user_agent)

        except Exception as es:

            print(f'Ошибка при создание браузера "{name_profile}" "{user_agent}" "{es}"')

            return False

        return browser

    def loop_write_in_cell(self, name_sheet, account_row, columns, over_status):

        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                SendlerOneCreate('').save_text(f'{NAME_SERVER} BoosterSeo: Не смог записать в столбец {columns} '
                                               f'в строчку "{account_row}" iter_job')

                return False

            res_write = self.google_alternate.new_write_in_cell(name_sheet, account_row, columns, over_status)

            if not res_write:
                self.google_alternate = ConnectGoogleCore()

                continue

            return res_write

    def write_value_by_google(self, _request, browser_profile):

        total_click = _request['complete_click'] + 1

        row_ = _request['row'] + 2

        columns_ = 3

        self.loop_write_in_cell(_request['name_sheet'], row_, columns_, total_click)

        ######################################################################

        columns_last_date = 6

        last_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.loop_write_in_cell(_request['name_sheet'], row_, columns_last_date, last_date)

        ######################################################################

        browser_profile['complete_click'] = browser_profile['complete_click'] + 1

        row_ = browser_profile['row'] + 2

        columns_ = 3

        self.loop_write_in_cell(browser_profile['name_sheet'], row_, columns_,
                                browser_profile['complete_click'])

        ######################################################################

        if browser_profile['complete_click'] < MAX_CLICK_ONE_ACCOUNT:
            self.list_profile.append(browser_profile)

        return True

    def _iter_requests(self):
        """Итерирую полученные запросы, выбираю браузерный профиль и создаю браузер"""

        for _request in self.list_requests:

            try:

                browser_profile = self.list_profile.pop(0)

            except Exception as es:
                print(f'Кончились профили для обработки запросов')
                return False

            target_request = _request['request']

            name_profile = browser_profile['name_profile']

            user_agent = browser_profile['user_agent']

            browser = self.start_profile(name_profile, user_agent)

            if not browser:
                continue

            try:

                res_farm = YandexFarmSearch(browser.driver, name_profile, target_request, self.dir_project,
                                            self.google_alternate, _request).start_job_search_target_site()

                if res_farm:

                    res_write = self.write_value_by_google(_request, browser_profile)

                    CoiceShab(browser.driver).start_choice()

                else:

                    self.list_profile.append(browser_profile)

                    continue

            finally:

                browser.driver.quit()
                try:
                    res_reboot = self.android_phone.start_reboot_ip()

                    if not res_reboot:
                        return 'reboot'

                except:
                    print(f'Не смог перезагрузить прокси')
                    return False

        return True

    def start_iter_job(self):

        res_iter_requests = self._iter_requests()

        return res_iter_requests
