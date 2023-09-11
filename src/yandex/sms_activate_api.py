import asyncio
from smsactivate.api import SMSActivateAPI

from settings import SMS_TOKEN


class SmsActivateApi:
    def __init__(self):
        self.api_key = SMS_TOKEN
        self.sa = SMSActivateAPI(self.api_key)
        self.country = 0

    def get_free_service(self, operator, servises):
        self.response = self.sa.getNumbersStatus(country=self.country, operator=f'{operator}')

        try:
            self.status = self.response[f'{servises}_{self.country}']

        except:
            self.status = self.response['message']

        return self.status

    def get_balance(self):
        self.balance = self.sa.getBalance()

    def get_number(self, services, operator):
        self.number = self.sa.getNumberV2(service=services, operator=operator, country=self.country)

        try:
            self.number_phone = self.number['phoneNumber']
            self.number_id = self.number['activationId']
        except:

            try:
                print(f'Ошибка при получения номера: {self.number["error"]}')
            except:
                pass

            return False

        return self.number

    def get_status(self, id_order):
        self.status = self.sa.getStatus(id_order)

        return self.status

    def set_status(self, id_order, status):
        self.status = self.sa.setStatus(id_order, status=status)

        return self.status
