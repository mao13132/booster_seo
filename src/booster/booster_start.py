from src.booster.get_requests import GetRequests


class BoosterStart:
    def __init__(self, google_alternate, driver):
        self.google_alternate = google_alternate
        self.driver = driver

    def booster_start(self):
        list_requests = GetRequests(self.google_alternate).get_job_requests()
