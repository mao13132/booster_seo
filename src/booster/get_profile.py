from settings import MAX_DAY_FARM


class GetProfile:
    def __init__(self, google_alternate):

        self.google_alternate = google_alternate

        self.name_sheets_requests = 'аккаунты'

        self.count_rows = 10000

        self.max_click_one_account = 5

        self.job_status = 'active'

    def get_active_profile(self, list_profiles):

        good_list = []

        for count, row in enumerate(list_profiles):

            try:

                name_profile, user_agent, count_click, status, login_and_password, date_create = row

            except:

                continue

            try:
                count_click = int(count_click)
            except:
                continue

            if status != self.job_status:
                continue

            if count_click >= self.max_click_one_account:
                self.google_alternate.write_in_cell(self.name_sheets_requests, count + 2, 4, 'Превышен лимит кликов')
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
        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        job_list_profiles = self.get_active_profile(list_profiles)

        return job_list_profiles

    def get_count_zero_profile(self):

        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        count = 0

        for _profile in list_profiles:

            status = _profile[3]

            if status.isdigit():

                status = int(status)

                if status == 0:
                    count += 1

        return count

    def get_account_farm(self):

        good_list = []

        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        if not list_profiles:
            return False

        for count_row, _profile in enumerate(list_profiles):

            status = _profile[3]

            if status.isdigit():

                status = int(status)

                if status < MAX_DAY_FARM:

                    _temp = {}

                    _temp['row'] = count_row + 2
                    _temp['_profile'] = _profile

                    good_list.append(_temp)

                else:
                    self.google_alternate.write_in_cell(self.name_sheets_requests, count_row + 2, 4,
                                                        'active')
                    print(f'BoosterSeo: Перевёл аккаунт {_profile[0]} в active')

        return good_list

    def get_last_row_profile(self):
        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        if not list_profiles:
            return False

        last_good_row = len(list_profiles) + 2

        return last_good_row
