import time
from datetime import datetime, timedelta

from settings import MAX_DAY_FARM, NAME_SERVER
from src.google.google_core import ConnectGoogleCore
from src.telegram_debug import SendlerOneCreate


class GetProfile:
    def __init__(self, google_alternate):

        self.google_alternate = google_alternate

        self.name_sheets_requests = 'аккаунты'

        self.count_rows = 10000

        self.max_click_one_account = 5

        self.job_status = 'active'

        self.stop_farm = timedelta(hours=12)

    def loop_write_in_cell(self, name_sheet, account_row, columns, over_status):

        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                SendlerOneCreate('').save_text(f'{NAME_SERVER} Booster Seo: Не смог записать в столбец {columns} '
                                               f'в строчку "{account_row}" get_profile')

                return False

            res_write = self.google_alternate.new_write_in_cell(name_sheet, account_row, columns, over_status)

            if not res_write:
                self.google_alternate = ConnectGoogleCore()

                continue

            return res_write

    def get_active_profile(self, list_profiles):

        good_list = []

        no_name_server = False

        for count, row in enumerate(list_profiles):

            try:

                name_profile, user_agent, count_click, status, login_and_password, date_create, name_server = row

            except:

                continue

            try:
                count_click = int(count_click)
            except:
                continue

            if status != self.job_status:
                continue

            if count_click >= self.max_click_one_account:
                # self.google_alternate.write_in_cell(self.name_sheets_requests, count + 2, 4, 'Превышен лимит кликов')

                self.loop_write_in_cell(self.name_sheets_requests, count + 2, 4, 'Превышен лимит кликов')

                continue

            if name_server.lower() != NAME_SERVER.lower():
                continue

            max_click = self.max_click_one_account - count_click

            _temp = {}

            _temp['name_profile'] = name_profile

            _temp['row'] = count

            _temp['user_agent'] = user_agent

            _temp['max_click'] = max_click

            _temp['complete_click'] = count_click

            _temp['name_sheet'] = self.name_sheets_requests

            good_list.append(_temp)

        return good_list

    def get_profile(self):
        for _try in range(4):

            list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:G{self.count_rows}')

            if not list_profiles:
                time.sleep(2)
                continue

            job_list_profiles = self.get_active_profile(list_profiles)

            return job_list_profiles

        print(f'Все попытки получить профили исчерпаны get_profile')

        return False

    def get_count_zero_profile(self):

        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:G{self.count_rows}')

        count = 0

        for _profile in list_profiles:

            status = _profile[3]

            server_name = _profile[6]

            if server_name.lower() != NAME_SERVER.lower():
                continue

            if status.isdigit():

                status = int(status)

                if status == 0:
                    count += 1

        return count

    def date_over_old_farm(self, _date):
        _date = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')

        now_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

        target_time = now_time - _date

        if target_time < self.stop_farm:
            return False

        return True

    def get_account_farm(self):

        good_list = []

        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:G{self.count_rows}')

        if list_profiles == []:
            return []

        if not list_profiles:
            return False

        for count_row, _profile in enumerate(list_profiles):

            status = _profile[3]

            date_account = _profile[5]

            name_server = _profile[6]

            if name_server != NAME_SERVER:
                continue

            check_date = self.date_over_old_farm(date_account)

            if not check_date:
                continue

            if status.isdigit():

                status = int(status)

                if status < MAX_DAY_FARM:

                    _temp = {}

                    _temp['row'] = count_row + 2
                    _temp['_profile'] = _profile

                    good_list.append(_temp)

                else:
                    self.loop_write_in_cell(self.name_sheets_requests, count_row + 2, 4,
                                            'active')
                    print(f'{NAME_SERVER} Booster Seo: Перевёл аккаунт {_profile[0]} в active')

        return good_list

    def get_last_row_profile(self):
        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        if not list_profiles:
            return False

        last_good_row = len(list_profiles) + 2

        return last_good_row
