# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime


def search_last_date(list_requests):
    no_date = True

    _temp_date = ''

    _temp_inx = -1

    for _ind, _req in enumerate(list_requests):
        last_date_row = _req['last_date']

        if last_date_row == '' or last_date_row == 0:
            continue

        last_date_row = datetime.strptime(last_date_row, '%Y-%m-%d %H:%M:%S')

        no_date = False

        if _temp_date == '':
            _temp_date = last_date_row
            _temp_inx = _ind
            continue

        if _temp_date < last_date_row:
            _temp_date = last_date_row
            _temp_inx = _ind

    if no_date:
        return 0

    if _temp_date == len(list_requests):
        return 0

    return _temp_inx
