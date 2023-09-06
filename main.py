import os
from datetime import datetime

from src.booster.booster_start import BoosterStart
from src.google.google_core import ConnectGoogleCore


def main():
    dir_project = os.getcwd()

    google_alternate = ConnectGoogleCore()

    res_booster = BoosterStart(google_alternate, dir_project).booster_start()

    print()


print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: начал работу')

if __name__ == '__main__':
    main()
