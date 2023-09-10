import os
from datetime import datetime

from src.android.android_core_one_step import android_core_one_step
from src.booster.booster_reg import BoosterReg
from src.booster.booster_start import BoosterStart
from src.google.google_core import ConnectGoogleCore


def main():
    dir_project = os.getcwd()

    android_phone = android_core_one_step()

    google_alternate = ConnectGoogleCore()

    # res_booster = BoosterStart(google_alternate, dir_project, android_phone).booster_start()

    res_reg = BoosterReg(google_alternate, dir_project, android_phone).start_reg()


if __name__ == '__main__':
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: начал работу')

    main()

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: окончил работу')
