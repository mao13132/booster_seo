import asyncio
import random

from src.yandex.stoper import Stoper


class Scroll:
    def __init__(self, driver):
        self.driver = driver
        self.storona = ['-', '+']
        self._list_scroll = [101, 77, 115, 131, 132, 71, 33]

    def scroll_mikro(self):
        self._temp_storona = random.choice(self.storona)

        self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {random.choice(self._list_scroll)})")
        asyncio.run(Stoper().stoper(0.2))
        self.driver.execute_script(
            f"window.scrollTo(0, window.scrollY {self._temp_storona} {random.choice(self._list_scroll)})")
