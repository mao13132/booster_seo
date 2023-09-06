import time

import uiautomator2 as u2


class Reboot_ip:
    def __init__(self, phone):
        self.d = phone.d

    def reboot_ip(self):
        count = 0
        while not self.reboot_shab_1():
            count += 1
            print(f'Android: пробую перезагрузить еще. Попытка: {count}')

            self.d.unlock()

            if count > 5:
                print(f'Android: Прерываю попытки смены IP кончились попытки {count}')
                return False
        return True

    def reboot_shab_1(self):

        respons = self.shab_takeip()
        if respons == False:
            return False

        self.samolet()

        print(f'Android: Засыпаю на 20 сек')
        time.sleep(20)

        self.samolet()

        return self.shab_takeip(self.ip)

    def shab_takeip(self, old_ip=''):

        self.run_browser()

        respons = self.check_browser()
        if respons == False:
            return False

        self.load_site('https://whoer.net/ru')
        respons = self.check_load_site()
        if respons == False:
            return False

        respons = self.get_ip()
        if respons == False:
            return False

        print(f'Android: текущий IP: {self.ip}')

        self.load_site('https://google.com', 1)

        if not old_ip == '':
            if old_ip == self.ip:
                print(f'Android: IP не сменился! Старый: {old_ip} новый: {self.ip}')
                return False
            else:
                print(f'Android: IP успешно изменён! Старый: {old_ip} новый: {self.ip}')
                return True

    def samolet(self):
        self.d.open_quick_settings()
        count = 0
        self._avia = 'режим'
        while self.d.xpath(f'//*[contains(@content-desc, "{self._avia}")]').wait_gone(timeout=1):
            count += 1
            if count > 10:
                print(f'Android: Попытки кончились. Не смог зайти в авиарежим')
                return False
            time.sleep(0.2)
        self.d.xpath(f'//*[contains(@content-desc, "{self._avia}")]').click()
        time.sleep(0.2)
        self.d.keyevent('home')
        return True

    def run_browser(self):
        self.d.app_start('com.android.chrome', use_monkey=True)
        return True

    def check_browser(self):
        count = 0
        while self.d.xpath('//*[contains(@resource-id, '
                           '"com.android.chrome:id/url_bar")]').wait_gone(timeout=3.0):
            if count > 10:
                print(f'Android: Не могу дождаться запуска браузера - выход')
                return False
            count += 1
            self.d.swipe_ext("down")
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

            if count > 10:

                print(f'Не смог дождаться загрузку сайта для проверки IP')

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

            return False