import random
import time
from datetime import datetime, timedelta

from settings import MAX_DAY_FARM
from src.booster._booster_farm_acc import _BoosterFarmAcc
from src.booster.get_profile import GetProfile
from src.browser.createbrowser import CreatBrowser
from src.google.google_core import ConnectGoogleCore


class BoosterFarmAcc:
    def __init__(self, google_alternate, dir_project, android_phone):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone

        self.stop_farm = timedelta(hours=12)

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

    def start_profile(self, name_profile, user_agent):

        try:

            browser = CreatBrowser(self.dir_project, name_profile, user_agent)

        except Exception as es:

            print(f'Ошибка при создание браузера farm "{name_profile}" "{user_agent}" "{es}"')

            return False

        return browser

    def date_over_old_farm(self, _date):
        _date = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')

        now_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

        target_time = now_time - _date

        if target_time < self.stop_farm:
            return False

        return True

    def iter_farm(self, list_account_farm):

        _farm_status = False

        for count, _reg_acc in enumerate(list_account_farm):

            try:

                _profile = _reg_acc['_profile']

                account_row = _reg_acc['row']

                name_profile = _profile[0]

                user_aget = _profile[1]

                status = int(_profile[3])

                login_password = _profile[4]

                date_account = _profile[5]

                check_date = self.date_over_old_farm(date_account)

                if not check_date:
                    continue

                _farm_status = True

                browser = self.start_profile(name_profile, user_aget)

                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: начинаю прогрев "{name_profile}"')

                res_reg = _BoosterFarmAcc(self.google_alternate, self.dir_project, self.android_phone,
                                          browser.driver, status, login_password).start_farm(account_row)

                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: закончил прогрев "{name_profile}"')


            finally:
                if _farm_status:

                    browser.driver.quit()

                    """Если прогревал аккаунт то перезагружаю IP"""
                    try:
                        self.android_phone.start_reboot_ip()

                        _farm_status = False

                    except:

                        print(f'Не смог перезагрузить прокси farm')

                        return False

        return True

    def start_farm(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Запущен режим прогрева аккаунтов моложе {MAX_DAY_FARM} дней')

        list_account_farm = self.get_account_farm_list()

        res_iter = self.iter_farm(list_account_farm)

        return res_iter
