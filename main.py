import os
from datetime import datetime

from settings import NAME_SERVER
from src.android.android_core_one_step import android_core_one_step
from src.android.rebook_ip import Reboot_ip
from src.booster.booster_farm_acc import BoosterFarmAcc
from src.booster.booster_reg import BoosterReg
from src.booster.booster_start import BoosterStart
from src.google.google_core import ConnectGoogleCore
from src.telegram_debug import SendlerOneCreate


def main():
    dir_project = os.getcwd()

    android_phone = android_core_one_step(dir_project)

    if not android_phone:
        return False

    google_alternate = ConnectGoogleCore()

    res_booster = BoosterStart(google_alternate, dir_project, android_phone).booster_start()

    if res_booster == 'reboot':
        return False

    res_reg = BoosterFarmAcc(google_alternate, dir_project, android_phone).start_farm()

    res_reg = BoosterReg(google_alternate, dir_project, android_phone).start_reg()


if __name__ == '__main__':
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {NAME_SERVER} Booster Seo: начал работу')
    try:
        main()
    except Exception as es:
        SendlerOneCreate('').save_text(f'{NAME_SERVER} Booster Seo: программа легла с ошибкой: "{es}"')

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {NAME_SERVER} Booster Seo: окончил работу')
