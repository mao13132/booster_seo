import random
import time
from datetime import datetime

from settings import MAX_REGISTRATION_ACCOUNT, NAME_SERVER
from src.booster._booster_reg import _BoosterReg
from src.booster.get_profile import GetProfile
from src.browser.createbrowser import CreatBrowser
from src.google.google_core import ConnectGoogleCore

from src.yandex.yandex_gen_accont_date import YandexAccaunt


class BoosterReg:
    def __init__(self, google_alternate, dir_project, android_phone):
        self.google_alternate = google_alternate
        self.dir_project = dir_project
        self.android_phone = android_phone

    def generate_data_new_user(self):
        name_account = YandexAccaunt.get_name()

        surname_account = YandexAccaunt.get_surname()

        name_profile = YandexAccaunt.get_name_profile(name_account, surname_account)

        login_account = f"{name_profile}{random.randint(10000, 99999)}"

        user_agent = YandexAccaunt.get_user_agent()

        password_account = YandexAccaunt.gen_password()

        _dict = {
            'name_account': name_account,
            'surname_account': surname_account,
            'name_profile': name_profile,
            'login_account': login_account,
            'user_agent': user_agent,
            'password_account': password_account,
        }

        return _dict

    def start_profile(self, name_profile, user_agent):

        try:

            browser = CreatBrowser(self.dir_project, name_profile, user_agent)

        except Exception as es:

            print(f'Ошибка при создание браузера reg "{name_profile}" "{user_agent}" "{es}"')

            return False

        return browser

    def get_last_row(self):

        count = 0

        count_try = 4

        while True:

            count += 1

            if count > count_try:
                # print(f'{NAME_SERVER} Booster Seo: Не смог получить последнюю строчку профилей')
                return 2

            count_zero = GetProfile(self.google_alternate).get_last_row_profile()

            if not count_zero:
                self.google_alternate = ConnectGoogleCore()

                continue

            return count_zero

    def iter_reg(self):

        _reg_status = False

        for _reg_acc in range(MAX_REGISTRATION_ACCOUNT):

            try:

                last_good_row = self.get_last_row()

                time.sleep(1)

                count_zero = GetProfile(self.google_alternate).get_count_zero_profile()

                if count_zero >= MAX_REGISTRATION_ACCOUNT:
                    print(f'{NAME_SERVER} Booster Seo: Зарегистрировано максимальное кол-во аккаунтов ({MAX_REGISTRATION_ACCOUNT})')
                    return True

                data_user = self.generate_data_new_user()

                _reg_status = True

                browser = self.start_profile(data_user['name_profile'], data_user['user_agent'])

                res_reg = _BoosterReg(self.google_alternate, self.dir_project, self.android_phone,
                                      browser.driver, data_user).start_reg(last_good_row)

                if res_reg == 'NO_BALANCE':
                    return 'NO_BALANCE'


            finally:
                if _reg_status:

                    browser.driver.quit()

                    """Если зарегистрировал то перезагружаю IP"""
                    try:
                        self.android_phone.start_reboot_ip()

                        _reg_status = False

                    except:

                        print(f'Не смог перезагрузить прокси reg')

        return True

    def start_reg(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'{NAME_SERVER} Booster Seo: Запущен режим регистрации аккаунтов')

        res_iter = self.iter_reg()

        return res_iter
