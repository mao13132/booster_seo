class GetRequests:
    def __init__(self, google_alternate):
        self.google_alternate = google_alternate
        self.name_sheets_requests = 'main'
        self.count_rows = 10000

    def calculate_request(self, list_requests):

        dooble_list = []

        good_list = []

        for count, row in enumerate(list_requests):

            try:
                _request, target_count, complete_count = row
            except:
                continue

            try:
                complete_count = int(complete_count)
                target_count = int(target_count)
            except:
                print(f'Не верное написание кол-во кликов')
                continue

            if complete_count >= target_count:
                continue

            if _request in dooble_list:
                continue

            dooble_list.append(_request)

            max_click = target_count - complete_count

            _temp = {}

            _temp['request'] = _request
            _temp['row'] = count
            _temp['max_click'] = max_click
            _temp['complete_click'] = complete_count

            good_list.append(_temp)

        return good_list

    def get_job_requests(self):
        list_requests = self.google_alternate.get_data_by_range(self.name_sheets_requests, f'A2:C{self.count_rows}')

        job_requests_list = self.calculate_request(list_requests)

        return job_requests_list
