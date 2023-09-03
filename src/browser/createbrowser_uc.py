import os
import platform

import undetected_chromedriver as uc

import getpass


class CreatBrowser:

    def __init__(self, dir_project, name_profile, user_agent):


        platform_to_os = platform.system()
        options = uc.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('ignore-certificate-errors')
        options.add_argument("--log-level=3")

        user_system = getpass.getuser()

        if platform_to_os == "Linux":
            path_dir = (f'/Users/{user_system}/Library/Application Support/Google/Chrome/{name_profile}')
            _patch = f"{dir_project}/src/browser/chromedriver.exe"
        else:
            path_dir = (f'C:\\Users\\{user_system}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')
            _patch = f"{dir_project}\\src\\browser\\chromedriver.exe"

        options.add_argument(f'--user-data-dir={path_dir}')

        options.add_argument(f'--proxy-server = {None}')

        options.add_argument(user_agent)

        self.driver = uc.Chrome(driver_executable_path=_patch, options=options)

        try:
            browser_version = self.driver.capabilities['browserVersion']
            driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print(f"\nБраузер: {browser_version} драйвер: {driver_version}")
        except:
            print(f'\nНе получилось определить версию uc браузера')
