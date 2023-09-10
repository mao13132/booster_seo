import random

from src.altastroy.shab1 import Shab1
from src.altastroy.shab2 import Shab2
from src.altastroy.shab3 import Shab3
from src.altastroy.shab4 import Shab4
from src.altastroy.shab5 import Shab5


class CoiceShab:
    def __init__(self, driver):
        self.driver = driver
        self.list_shab = {
            0: Shab1(self.driver).start_shab,
            1: Shab2(self.driver).start_shab,
            2: Shab3(self.driver).start_shab,
            3: Shab4(self.driver).start_shab,
            4: Shab5(self.driver).start_shab,
        }

    def start_choice(self):

        try:

            start_ = self.list_shab[random.choice([x for x in self.list_shab.keys()])]()

        except Exception as es:

            print(f'Ошибка в работе шаблона имитатора "{es}"')

            return False

        return True
