from src.android.adb_modul import Check_emul
from src.android.android_run import Connect_phone


def android_core_one_step():
    serial = Check_emul().check_emul()

    if not serial:
        return False

    print(f'Android: Подключился к устройству серийный номер: {serial}')

    andrushka = Connect_phone(serial)

    return andrushka
