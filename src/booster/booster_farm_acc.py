import random
import time
from datetime import datetime

from settings import MAX_REGISTRATION_ACCOUNT, MAX_DAY_FARM
from src.booster._booster_reg import _BoosterReg
from src.booster.get_profile import GetProfile
from src.browser.createbrowser import CreatBrowser
from src.google.google_core import ConnectGoogleCore

from src.yandex.yandex_gen_accont_date import YandexAccaunt


class BoosterFarmAcc:
    def __init__(self, google_alternate, dir_project, android_phone):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone

    def get_account_farm_list(self):

        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                print(f'BoosterSeo: Не смог получить список профилей для прогрева')
                return False

            account_farm_list = GetProfile(self.google_alternate).get_account_farm()

            if not account_farm_list:
                self.google_alternate = ConnectGoogleCore()

                continue

            return account_farm_list

    def iter_farm(self, list_account_farm):

        _farm_status = False

        for _reg_acc in range(list_account_farm):

            try:

                last_good_row = self.get_last_row()

                time.sleep(1)

                count_zero = GetProfile(self.google_alternate).get_count_zero_profile()

                if count_zero >= MAX_REGISTRATION_ACCOUNT:
                    print(f'BoosterSeo: Зарегистрировано максимальное кол-во аккаунтов ({MAX_REGISTRATION_ACCOUNT})')
                    return True

                data_user = self.generate_data_new_user()

                _farm_status = True

                browser = self.start_profile(data_user['name_profile'], data_user['user_agent'])

                res_reg = _BoosterReg(self.google_alternate, self.dir_project, self.android_phone,
                                      browser.driver, data_user).start_reg(last_good_row)


            finally:
                if _farm_status:

                    browser.driver.quit()

                    """Если зарегистрировал то перезагружаю IP"""
                    try:
                        self.android_phone.start_reboot_ip()

                        _farm_status = False

                    except:

                        print(f'Не смог перезагрузить прокси')

                        return False

        return True

    def start_farm(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Запущен режим прогрева аккаунтов моложе {MAX_DAY_FARM} дней')

        list_account_farm = self.get_account_farm_list()

        res_iter = self.iter_farm(list_account_farm)

        return res_iter
