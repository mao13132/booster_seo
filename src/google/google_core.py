import time
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials

import gspread

from settings import ID_SHEET, NAME_SERVER, API_KEY_GOOGLE

from src.telegram_debug import SendlerOneCreate


class ConnectGoogleCore:
    def __init__(self):
        self.micro_sleep = 1

        json_keyfile = f'src/google/keys/{API_KEY_GOOGLE}'

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

        gc = gspread.authorize(credentials)

        self.sheet = gc.open_by_key(ID_SHEET)

    def get_name_sheets(self):

        list_title_sheet = self.sheet.worksheets()

        return [x.title for x in list_title_sheet]

    def get_range_date_columns(self, name_sheet, range):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            list_columns = worksheet.range(range)

        except Exception as es:
            msg = f'{NAME_SERVER} Ошибка get_range_date_columns: "{es}"'

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return False

        return list_columns

    def write_title(self, dict_, name_sheet, now_date):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            for _count in range(5):
                _columns = dict_[_count][f'range{_count + 1}']['job_index_col']

                worksheet.update_cell(2, _columns, now_date)

        except Exception as es:
            msg = f'{NAME_SERVER} Ошибка write_title: "{es}"'

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return False

        return True

    def write_in_cell(self, name_sheet, row, columns, data_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.update_cell(row, columns, data_)

        except Exception as es:
            msg = f'{NAME_SERVER} Ошибка write_in_cell: "{es}"'

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return False

        return True

    def get_data_by_range(self, name_sheet, range_):

        worksheet = self.sheet.worksheet(name_sheet)

        return worksheet.get_values(range_)

    def write_data_from_exel_file(self, good_range_date, name_sheet, count_google_row,
                                  position, rez_ocenka, popular_request, trade_product, popular_total):

        try:

            if position == '':
                print(f'Пустое значение словить')

            worksheet = self.sheet.worksheet(name_sheet)

            position_columns = good_range_date[0]['range1']['job_index_col']

            job_row = 3 + count_google_row

            worksheet.update_cell(job_row, position_columns, position)


        except Exception as es:
            msg = f'{NAME_SERVER} Ошибка write_data_from_exel_file: "{es}"'

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return False

        return True
