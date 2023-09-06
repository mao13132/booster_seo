from src.browser.createbrowser import CreatBrowser
from src.telegram_debug import SendlerOneCreate
from src.yandex.yandex_start_search import YandexFarmSearch


class IterJob:
    def __init__(self, google_alternate, list_requests, list_profile, dir_project):
        self.google_alternate = google_alternate
        self.list_requests = list_requests
        self.list_profile = list_profile
        self.dir_project = dir_project

    def start_profile(self, name_profile, user_agent):

        try:
            browser = CreatBrowser(self.dir_project, name_profile, user_agent)
        except Exception as es:

            print(f'Ошибка при создание браузера "{name_profile}" "{user_agent}" "{es}"')

            return False

        return browser

    def _iter_requests(self):
        """Итерирую полученные запросы, выбираю браузерный профиль и создаю браузер"""

        for _request in self.list_requests:

            try:
                browser_profile = self.list_profile.pop(0)
            except Exception as es:
                SendlerOneCreate('').save_text(f'Кончились профили для обработки запросов')
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
                    total_click = _request['complete_click'] + 1

                    row_ = _request['row'] + 2

                    columns_ = 3

                    res_write = self.google_alternate.write_in_cell(_request['name_sheet'], row_, columns_, total_click)

                    total_click = browser_profile['complete_click'] + 1

                    if total_click < browser_profile['max_click']:
                        self.list_profile.append(browser_profile)

                    row_ = _request['row'] + 1

                    columns_ = 3

                    res_write = self.google_alternate.write_in_cell(browser_profile['name_sheet'], row_, columns_,
                                                                    total_click)

                    print(f'Запуск шаблона по фарму')


                else:
                    continue

            finally:
                print(f'перезагрузка прокси')
                browser.driver.quit()

            print()

        return True

    def start_iter_job(self):
        res_iter_requests = self._iter_requests()

        print()

        return res_iter_requests
