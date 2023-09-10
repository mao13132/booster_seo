import random
from datetime import datetime

from settings import MAX_REGISTRATION_ACCOUNT
from src.booster._booster_reg import _BoosterReg
from src.browser.createbrowser import CreatBrowser

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

            print(f'Ошибка при создание браузера "{name_profile}" "{user_agent}" "{es}"')

            return False

        return browser


    def iter_reg(self):
        for _reg_acc in range(MAX_REGISTRATION_ACCOUNT):

            data_user = self.generate_data_new_user()

            try:

                browser = self.start_profile(data_user['name_profile'], data_user['user_agent'])

                res_reg = _BoosterReg(self.google_alternate, self.dir_project, self.android_phone,
                                      browser.driver, data_user).start_reg()

                print()

            finally:
                browser.driver.quit()

        return True

    def start_reg(self):
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'BoosterSeo: Запущен режим регистрации {MAX_REGISTRATION_ACCOUNT} аккаунтов')

        res_iter = self.iter_reg()

        return res_iter
