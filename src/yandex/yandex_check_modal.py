from selenium.webdriver.common.by import By


class YandexCheckModal:
    def __init__(self, driver):
        self.driver = driver

    def _check_modal(self):
        try:
            modal = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'DeclineButtonOuter')]")
        except:
            return False

        return True

    def close_modal(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'DeclineButtonOuter')]").click()
        except:
            return False

        return True

    def start_check_modal(self):
        """Проверка на всплывающее окно при первом запуске учётной записи"""

        res_modal = self._check_modal()

        if not res_modal:
            return True

        res_close = self.close_modal()

        return res_close
