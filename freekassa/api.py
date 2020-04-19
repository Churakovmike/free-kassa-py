import requests
import hashlib


class FreeKassaApi:
    base_url = 'https://www.free-kassa.ru/api.php'
    base_form_url = 'http://www.free-kassa.ru/merchant/cash.php'
    base_export_order_url = 'https://www.free-kassa.ru/export.php'
    wallet_api_url = 'https://www.fkwallet.ru/api_v1.php'

    def __init__(self, merchant_id, first_secret, second_secret, wallet_id):
        self.merchant_id = merchant_id
        self.first_secret = first_secret
        self.second_secret = second_secret
        self.wallet_id = wallet_id

    def send_request(self, params, method='post'):
        return requests.__dict__[method](self.base_url, params=params)

    def get_balance(self):
        """

        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            's': self.generate_api_signature(),
            'action': 'get_balance',
        }
        print(params)
        return self.send_request(params=params)

    def generate_api_signature(self):
        """
        Generate api signature
        :return:str
        """
        return hashlib.md5(str(self.merchant_id).encode('utf-8') + str(self.second_secret).encode('utf-8')).hexdigest()
