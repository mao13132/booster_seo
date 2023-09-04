from src.browser.createbrowser_uc import CreatBrowser
from src.telegram_debug import SendlerOneCreate
from src.yandex.yandex_farm_search import YandexFarmSearch


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
                SendlerOneCreate('').save_text(f'Кончились профили для обработки запросов "{es}"')
                continue

            target_request = _request['request']

            name_profile = browser_profile['name_profile']

            user_agent = browser_profile['user_agent']

            browser = self.start_profile(name_profile, user_agent)

            if not browser:
                continue

            try:

                res_farm = YandexFarmSearch(browser.driver, name_profile, target_request).start_job_search_target_site()

            finally:
                browser.driver.quit()

            print()

        return True

    def start_iter_job(self):
        res_iter_requests = self._iter_requests()

        print()
