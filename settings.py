import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

MAX_CLICK_ONE_ACCOUNT = 5  # Максимальное кол-во кликов с 1 аккаунта

MAX_REGISTRATION_ACCOUNT = 16  # Максимальный запас новых аккаунтов

MAX_COUNT_PAGE = 10  # Максимальная страница до которой ведётся поиск целевого сайта

MAX_DAY_FARM = 3  # Максимальное кол-во дней прогрева аккаунтов

USE_PROXY = False

PROXY_HOST = '192.168.0.100'

PROXY_PORT = 8083

PROXY_USER = 'admin'

PROXY_PASS = '123123'

API_KEY_GOOGLE = 'booster_seo.json'

NAME_SERVER = 'main_razrabotka'

ID_SHEET = os.getenv('ID_SHEET')

CAPTCHA_TOKEN = os.getenv('CAPTCHA_TOKEN')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

SMS_TOKEN = os.getenv('SMS_TOKEN')
