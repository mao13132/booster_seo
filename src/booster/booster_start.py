from datetime import datetime

from settings import NAME_SERVER
from src.booster.get_profile import GetProfile
from src.booster.get_requests import GetRequests
from src.booster.iter_job import IterJob
from src.telegram_debug import SendlerOneCreate


class BoosterStart:
    def __init__(self, google_alternate, dir_project, android_phone):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone

    def booster_start(self):
        list_requests = GetRequests(self.google_alternate).get_job_requests()

        if list_requests == [] or not list_requests:
            SendlerOneCreate('').save_text(f'{NAME_SERVER} Booster Seo: Список запросов пуст. Засыпаю на 12 часов')
            return []

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Получил список из {len(list_requests)} запросов')

        list_profile = GetProfile(self.google_alternate).get_profile()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Получил список из {len(list_profile)} профилей')

        if list_profile == []:
            SendlerOneCreate('').save_text(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                                           f'{NAME_SERVER} Booster Seo: Нет профилей для работы. Засыпаю на 12 часов')

            return []

        res_iter_job = IterJob(self.google_alternate, list_requests,
                               list_profile, self.dir_project, self.android_phone).start_iter_job()

        return res_iter_job
