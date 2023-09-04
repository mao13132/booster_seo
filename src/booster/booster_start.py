from src.booster.get_profile import GetProfile
from src.booster.get_requests import GetRequests
from src.booster.iter_job import IterJob
from src.telegram_debug import SendlerOneCreate


class BoosterStart:
    def __init__(self, google_alternate, dir_project):
        self.google_alternate = google_alternate
        self.dir_project = dir_project

    def booster_start(self):
        list_requests = GetRequests(self.google_alternate).get_job_requests()

        if list_requests == []:
            SendlerOneCreate('').save_text('Список запросов пуст')
            return []

        print(f'Получил список из {len(list_requests)} запросов')

        list_profile = GetProfile(self.google_alternate).get_profile()

        print(f'Получил список из {len(list_profile)} профилей')

        if list_profile == []:
            SendlerOneCreate('').save_text('Нет профилей для работы')
            return []

        res_iter_job = IterJob(self.google_alternate, list_requests,
                               list_profile, self.dir_project).start_iter_job()

        print()


