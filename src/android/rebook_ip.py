import time
from datetime import datetime

import uiautomator2 as u2


class Reboot_ip:
    def __init__(self, phone):
        self.d = phone.d

    def reboot_ip(self):
        count = 0
        while not self.reboot_shab_1():
            count += 1
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'Android: пробую перезагрузить еще. Попытка: {count}')

            self.d.unlock()

            no_internet = self.check_no_internet()

            if no_internet:
                self.samolet()

            if count > 10:
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'Android: Прерываю попытки смены IP кончились попытки {count}')
                return False
        return True

    def reboot_shab_1(self):

        get_ip = self.shab_takeip()

        if get_ip == False:
            return False

        self.samolet()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
              f'Android: Засыпаю на 20 сек')
        time.sleep(20)

        self.samolet()

        res_reboot = self.shab_takeip(get_ip)

        return res_reboot

    def shab_takeip(self, old_ip=''):

        import stun
        ip_ = stun.get_ip_info()[1]

        if ip_ is None:
            ip_ = old_ip

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: текущий IP: {ip_}')

        # self.load_site('https://google.com', 1)

        if not old_ip == '':
            if old_ip == ip_:
                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: IP не сменился! Старый: {old_ip} новый: {ip_}')
                return False
            else:
                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: IP успешно изменён! Старый: {old_ip} новый: {ip_}')
                return True

        return ip_

    def samolet(self):
        self.d.open_quick_settings()
        count = 0
        self._avia = 'режим'
        while self.d.xpath(f'//*[contains(@content-desc, "{self._avia}")]').wait_gone(timeout=1):
            count += 1
            if count > 10:
                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                    f'Android: Попытки кончились. Не смог зайти в авиарежим')
                return False
            time.sleep(0.2)
        self.d.xpath(f'//*[contains(@content-desc, "{self._avia}")]').click()
        time.sleep(0.2)
        self.d.keyevent('home')
        return True

    def run_browser(self):

        self.d.keyevent('home')

        self.d.app_start('com.android.chrome', use_monkey=True)
        return True

    def check_browser(self):
        count = 0
        while self.d.xpath('//*[contains(@resource-id, '
                           '"com.android.chrome:id/url_bar")]').wait_gone(timeout=3.0):

            if count > 10:
                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Android: Не могу дождаться запуска браузера - выход')
                return False
            count += 1
            self.d.swipe_ext("down")
            time.sleep(1)

        return True

    def check_no_internet(self):
        count = 0
        while self.d.xpath(f'//*[contains(@resource-id, "airplane")]').wait_gone(timeout=3.0):

            if count > 2:
                return False

            count += 1
            time.sleep(1)

        return True

    def load_site(self, url, time_withe=3):
        self.d.xpath('//*[contains(@resource-id, '
                     '"com.android.chrome:id/url_bar")]').click()

        time.sleep(3)

        self.d(resourceId="com.android.chrome:id/url_bar", clickable=True).send_keys(url)

        time.sleep(1)

        self.d.press('enter')

        time.sleep(time_withe)

        return True

    def check_load_site(self):

        count = 0

        while self.d.xpath('//*[@content-desc="Мой IP: "]').wait_gone(timeout=1):

            if count > 2:
                try:
                    self.d.xpath('//*[@text="Мой IP: "]')
                    return True
                except:
                    pass

            if count > 10:
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                      f'Android: не смог дождаться загрузку сайта для проверки IP')

                return False

            count += 1

            time.sleep(0.3)

        return True

    def get_ip(self):

        try:

            self.ip = self.d.xpath('//*[contains(@content-desc, "Мой IP:")]'
                                   '//following-sibling::android.view.View').get().attrib['content-desc']
            return True
        except:
            pass

        try:

            self.ip = self.d.xpath('//*[contains(@text, "Мой IP:")]'
                                   '//following-sibling::android.widget.TextView').get().attrib['text']
            return True
        except:
            pass

        return False
