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

    def write_in_cell(self, name_sheet, row, columns, data_):

        for _try in range(2):

            try:

                worksheet = self.sheet.worksheet(name_sheet)

                worksheet.update_cell(row, columns, data_)

            except Exception as es:
                print(f'Отлов ошибки write_in_cell "{es}"')
                continue

            return True

        msg = f'{NAME_SERVER} Исчерпал все попытки google_core write_in_cell: ""'

        print(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def new_write_in_cell(self, name_sheet, row, columns, data_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.update_cell(row, columns, data_)

        except Exception as es:
            print(f'Отлов ошибки new_write_in_cell "{es}"')

            return False

        return True

    def write_in_range_account(self, name_sheet, row, data_):

        for _try in range(2):

            try:

                worksheet = self.sheet.worksheet(name_sheet)

                worksheet.update(f'A{row}:F{row}', [data_])

            except Exception as es:
                print(f'Отлов Ошибки "{es}"')
                continue

            return True

        msg = f'{NAME_SERVER} Исчерпал все попытки google_core write_in_range_account ""'

        print(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def get_data_by_range(self, name_sheet, range_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)
        except Exception as es:
            print(f'Отлов Ошибка при работе с get_data_by_range "{es}"')
            return False

        return worksheet.get_values(range_)
