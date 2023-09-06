import time

import uiautomator2 as u2
from src.android.rebook_ip import *

class Connect_phone:
    def __init__(self, serial_phone):
        self.serial_phone = serial_phone
        self.d = u2.connect(serial_phone)
        self.d.settings['wait_timeout'] = 4

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


        if not Reboot_ip(self).reboot_ip():
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: Не смог сменить IP останавливаю')
            return False

        return True
