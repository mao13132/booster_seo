import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

API_KEY_GOOGLE = 'booster_seo.json'

ID_SHEET = os.getenv('ID_SHEET')

NAME_SERVER = 'server_ip'

MAX_CLICK_ONE_ACCOUNT = 5

MAX_REGISTRATION_ACCOUNT = 5

MAX_COUNT_PAGE = 10

PROXY_HOST = '192.168.0.100'

PROXY_PORT = 8083

PROXY_USER = 'admin'

PROXY_PASS = '123123'

# LINK_RELOAD = 'http://176.9.113.111:20005/?command=switch&api_key=gNMLTBja2JNqnZWZPcvi&m_key=RBsxNJGh3A&port=21431'

CAPTCHA_TOKEN = os.getenv('CAPTCHA_TOKEN')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
