import subprocess
import time

import uiautomator2 as u2

from settings import NAME_SERVER
from src.android.rebook_ip import *
from src.telegram_debug import SendlerOneCreate


class Connect_phone:
    def __init__(self, serial_phone, dir_project):
        self.serial_phone = serial_phone
        self.d = u2.connect(serial_phone)
        self.d.settings['wait_timeout'] = 4
        self.dir_project = dir_project

    def __str__(self):
        return f'Android: информация о подключенном устройстве {self.d.info}'

    def check_lock(self):
        if self.d.info['screenOn']:
            return True
        else:
            return False

    def start_reboot_ip(self):

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: смена IP')

        if not self.check_lock():
            self.d.unlock()
            time.sleep(2)
            self.d.keyevent('home')

        for _try in range(2):

            res_reboot_ip = Reboot_ip(self).reboot_ip()

            if not res_reboot_ip:
                process_ = subprocess.run(
                    f"cd {self.dir_project}\\src\\android & adb.exe & adb reboot {self.serial_phone}",
                    shell=True)

                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: Начинаю перезагружать телефон. '
                      f'Засыпаю на 3 минуты')

                time.sleep(180)

                continue

            return True

        _screen = False

        try:
            name_file = r"src/screen/mobile.jpg"
            self.d.screenshot(name_file)
            _screen = name_file
        except:
            pass

        if not _screen:
            SendlerOneCreate('').save_text(
                f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                f'{NAME_SERVER} Android: Не смог сменить IP останавливаю')
        else:

            SendlerOneCreate('').send_file(
                f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {NAME_SERVER} '
                f'Android: Не смог сменить IP останавливаю', _screen)

        return False
