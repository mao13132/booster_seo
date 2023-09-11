import time
from datetime import datetime

from ppadb.client import Client as AdbClient
import os

import subprocess


class Check_emul:
    """pip install pure-python-adb Что бы завелась мобила, надо в cmd зайти в каталог с adb.exe
    и запустить его и после запустить команду adb devices. Что бы запустить редактор xpatch в вебе
    надо в консоле прописать python -m weditor"""

    def __init__(self):
        if not os.path.exists(r'src/android/adb.exe'):
            print(f'Ошибка: Не обнаружен adb.exe')
            return

        self.client = AdbClient(host="127.0.0.1", port=5037)

    def connect_to_adb(self):
        return True

    def check_emul(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'Android: Начинаю подключение к телефону')

        for _try in range(5):

            try:

                list_device = self.client.devices()

            except Exception as es:
                if 'WinError 10061' in str(es):
                    process_ = subprocess.run("cd src\\android & adb.exe & adb devices -l", shell=True)

                    continue

            if list_device == []:
                time.sleep(1)
                continue

            try:
                serial = self.client.devices()[0].serial
            except Exception as es:
                print(f'Android: При подключение к девайсу произошла ошибка {es}')

                continue

            return serial

        print(f'Android: Не обнаружил ни одного устройства')

        return False
