class GetProfile:
    def __init__(self, google_alternate):
        self.google_alternate = google_alternate
        self.name_sheets_requests = 'аккаунты'
        self.count_rows = 10000
        self.max_click_one_account = 5
        self.job_status = 'active'

    def get_active_profile(self, list_profiles):
        dooble_list = []

        good_list = []

        for count, row in enumerate(list_profiles):

            try:
                name_profile, user_agent, count_click, status, login_and_password, date_create = row
            except:
                continue

            try:
                count_click = int(count_click)
            except:
                print(f'Не верное написание кол-во кликов')
                continue

            if status != self.job_status:
                continue

            if count_click >= self.max_click_one_account:
                self.google_alternate.write_in_cell(self.name_sheets_requests, count + 2, 4, 'Превышен лимит кликов')
                continue

            max_click = self.max_click_one_account - count_click

            _temp = {}

            _temp['name_profile'] = name_profile
            _temp['user_agent'] = user_agent
            _temp['max_click'] = max_click

            good_list.append(_temp)

        return good_list

    def get_profile(self):
        list_profiles = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:F{self.count_rows}')

        job_list_profiles = self.get_active_profile(list_profiles)

        return job_list_profiles
