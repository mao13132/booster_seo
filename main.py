import os
from datetime import datetime

from src.booster.booster_start import BoosterStart
from src.browser.createbrowser_uc import CreatBrowser
from src.google.google_core import ConnectGoogleCore

def start_profile(dir_project):
    user_agent = f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 f"Chrome/114.0.0.0 Safari/537.36"

    user_profile = 'Profile0'

    try:
        browser = CreatBrowser(dir_project, user_profile, user_agent)
    except Exception as es:

        print(f'Ошибка при создание браузера "{user_profile}" "{user_agent}" "{es}"')

        return False

    return browser

def main():
    dir_project = os.getcwd()

    google_alternate = ConnectGoogleCore()

    # browser = start_profile(dir_project)
    #
    # if not browser:
    #     return False

    res_booster = BoosterStart(google_alternate, 'browser.driver').booster_start()

    print()





print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} начал работу')

if __name__ == '__main__':
    main()
