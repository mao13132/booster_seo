from selenium.webdriver.common.by import By


class YandexCheckModal:
    def __init__(self, driver):
        self.driver = driver

    def _check_modal(self):
        try:

            modal = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'DeclineButtonOuter')]").click()

            return True

        except:
            pass
        try:

            modal = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'Modal-Content')]/button").click()

            return True

        except:
            pass

        return False

    def close_modal(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'DeclineButtonOuter')]").click()
        except:
            return False

        return True

    def start_check_modal(self):
        """Проверка на всплывающее окно при первом запуске учётной записи"""

        res_modal = self._check_modal()

        return res_modal
