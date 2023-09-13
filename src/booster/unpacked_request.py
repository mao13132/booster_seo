# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

def unpacked_request(_req):
    _request = ''

    target_count = 0

    complete_count = 0

    count_page = 0

    count_row = 0

    last_date = ''

    start_page = 0

    start_row = 0

    start_date = ''

    for count, _val in enumerate(_req):
        if _val == '':
            _val = 0

        if count == 0:
            _request = _val
        elif count == 1:
            target_count = _val
        elif count == 2:
            complete_count = _val
        elif count == 3:
            count_page = _val
        elif count == 4:
            count_row = _val
        elif count == 5:
            last_date = _val
        elif count == 6:
            start_page = _val
        elif count == 7:
            start_row = _val
        elif count == 8:
            start_date = _val

    return _request, target_count, complete_count, count_page, count_row, last_date, start_page, start_row, start_date
