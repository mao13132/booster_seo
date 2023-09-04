import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

API_KEY_GOOGLE = 'booster_seo.json'

ID_SHEET = os.getenv('ID_SHEET')

NAME_SERVER = 'server_ip'

MAX_CLICK_ONE_ACCOUNT = 5
