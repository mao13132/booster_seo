import os
import platform
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import zipfile

import getpass

from src.browser.create_proxy import manifest_json, background_js


class CreatBrowser:
    """Класс создаёт браузер с настройками.
    Параметр create_head принимает или True или False обозначает что будет ли появляться браузер
    """

    def __init__(self, dir_project, name_profile, user_agent):

        proxy = True

        options = webdriver.ChromeOptions()

        user_system = getpass.getuser()

        options.add_argument(f"user-agent={user_agent}")

        path_dir = (f'C:\\Users\\{user_system}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')

        _patch = f"{dir_project}\\src\\browser\\chromedriver.exe"

        s = Service(executable_path=_patch)

        options.add_argument(f'--user-data-dir={path_dir}')

        # options.add_argument("--headless")  # скрываем браузер

        prefs = {"enable_do_not_track": True}

        options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        options.add_argument("--disable-infobars")

        options.add_argument("--disable-bundled-ppapi-flash")

        options.add_argument("--disable-application-cache")

        options.add_argument("window-size=1920,939")

        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('ignore-certificate-errors')
        options.add_argument("--log-level=3")

        if proxy:
            plugin_file = f"{dir_project}\\src\\browser\\proxy_auth_plugin.zip"

            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)

            options.add_extension(plugin_file)

        tz_params = {'timezoneId': 'Asia/Almaty'}

        self.driver = webdriver.Chrome(service=s, options=options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })

        self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

        try:
            browser_version = self.driver.capabilities['browserVersion']
            driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Браузер: {browser_version} драйвер: {driver_version}')
        except:
            print(f'\nНе получилось определить версию uc браузера')
