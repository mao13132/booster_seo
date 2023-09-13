from datetime import datetime

from src.android.adb_modul import Check_emul
from src.android.android_run import Connect_phone


def android_core_one_step(dir_project):
    serial = Check_emul().check_emul(dir_project)

    if not serial:
        return False

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
          f'Android: Подключился к устройству серийный номер: {serial}')

    andrushka = Connect_phone(serial)

    return andrushka
