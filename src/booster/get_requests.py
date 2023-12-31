import time
from datetime import datetime

from settings import NAME_SERVER
from src.booster.loop_write_in_cell import LoopWriteInCell
from src.booster.unpacked_request import unpacked_request


class GetRequests:
    def __init__(self, google_alternate):
        self.google_alternate = google_alternate
        self.name_sheets_requests = 'main'
        self.count_rows = 10000

    def calculate_request(self, list_requests):

        dooble_list = []

        good_list = []

        no_name_server = False

        for count, row in enumerate(list_requests):

            try:
                _request, target_count, complete_count, count_page, count_row, last_date, start_page, start_row, \
                    start_date, name_server = unpacked_request(row)
            except:
                continue

            try:
                complete_count = int(complete_count)
                target_count = int(target_count)
            except:
                continue

            if complete_count >= target_count:
                continue

            if _request in dooble_list:
                continue

            if name_server.lower() != NAME_SERVER.lower() and name_server != '':
                continue

            if name_server == '':
                if no_name_server:
                    time.sleep(3)

                LoopWriteInCell(self.google_alternate) \
                    .loop_write_in_cell(self.name_sheets_requests, count + 2, 10, NAME_SERVER)

                no_name_server = True

            dooble_list.append(_request)

            max_click = target_count - complete_count

            _temp = {}

            _temp['request'] = _request
            _temp['row'] = count
            _temp['max_click'] = max_click
            _temp['complete_click'] = complete_count
            _temp['name_sheet'] = self.name_sheets_requests
            _temp['last_date'] = last_date
            _temp['start_page'] = start_page

            good_list.append(_temp)

        return good_list

    def get_job_requests(self):

        for _try in range(3):

            list_requests = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:J{self.count_rows}')

            if not list_requests:
                time.sleep(5)
                continue

            job_requests_list = self.calculate_request(list_requests)

            return job_requests_list

        print(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {NAME_SERVER} '
            f'Booster Seo: кончились попытки получить запросы')

        return False
