# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import NAME_SERVER
from src.google.google_core import ConnectGoogleCore
from src.telegram_debug import SendlerOneCreate


class LoopWriteInCell:
    def __init__(self, google_alternate):

        self.google_alternate = google_alternate

    def loop_write_in_cell(self, name_sheet, account_row, columns, data_):
        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                SendlerOneCreate('').save_text(f'{NAME_SERVER} Booster Seo: Не смог записать в столбец {columns} '
                                               f'в строчку "{account_row}" get_profile')

                return False

            res_write = self.google_alternate.new_write_in_cell(name_sheet, account_row, columns, data_)

            if not res_write:
                self.google_alternate = ConnectGoogleCore()

                continue

            return res_write
