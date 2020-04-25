import requests
import hashlib


class FreeKassaApi:
    base_url = 'https://www.free-kassa.ru/api.php'
    base_form_url = 'http://www.free-kassa.ru/merchant/cash.php'
    base_export_order_url = 'https://www.free-kassa.ru/export.php'
    wallet_api_url = 'https://www.fkwallet.ru/api_v1.php'

    def __init__(self, merchant_id, first_secret, second_secret, wallet_id, wallet_api_key=''):
        self.merchant_id = merchant_id
        self.first_secret = first_secret
        self.second_secret = second_secret
        self.wallet_id = wallet_id
        self.wallet_api_key = wallet_api_key

    def send_request(self, params, url=None, method='post'):
        """
        Send request to freekassa api
        :param url:
        :param params:params
        :param method:method
        :return:
        """
        if url is None:
            url = self.base_url

        return requests.__dict__[method](url, params=params)

    def get_balance(self):
        """
        Get merchant balance
        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            's': self.generate_api_signature(),
            'action': 'get_balance',
        }

        return self.send_request(params=params)

    def get_order(self, order_id='', int_id=''):
        """

        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            's': self.generate_api_signature(),
            'action': 'check_order_status',
            'order_id': order_id,
            'intid': int_id,
        }

        return self.send_request(params=params)

    def withdraw(self, amount, currency):
        """

        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            'currency': currency,
            'amount': amount,
            's': self.generate_api_signature(),
            'action': 'payment',
        }

        return self.send_request(params=params)

    def invoice(self, email, amount, description):
        """

        :param email:
        :param amount:
        :param description:
        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            'email': email,
            'amount': amount,
            'desc': description,
            's': self.generate_api_signature(),
            'action': 'create_bill',
        }

        return self.send_request(params)

    def get_wallet_balance(self):
        """

        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': self.generate_wallet_signature(),
            'action': self.get_balance(),
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def wallet_withdraw(self, purse, amount, currency, description, disable_exchange=1):
        """
        @todo: add generate tuple hash
        :param purse:
        :param amount:
        :param currency:
        :param description:
        :param disable_exchange:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'purse': purse,
            'amount': amount,
            'desc': description,
            'disable_exchange': disable_exchange,
            'currency': currency,
            'sign': '',
            'action': 'cashout',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_operation_status(self, payment_id):
        """
        @todo: todo
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'payment_id': payment_id,
            'sign': '',
            'action': 'get_payment_status',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def transfer_money(self, purse, amount):
        """
        @todo: todo
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'purse': purse,
            'amount': amount,
            'sign': '',
            'action': 'transfer',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def online_payments(self, service_id, account, amount):
        """
        @todo: todo
        :param service_id:
        :param account:
        :param amount:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'service_id': service_id,
            'account': account,
            'amount': amount,
            'sign': '',
            'action': 'online_payment',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_online_services(self):
        """
        @todo: todo
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': '',
            'action': 'providers',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_online_payment_status(self, payment_id):
        """
        @todo: todo
        :param payment_id:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'payment_id': payment_id,
            'sign': '',
            'action': 'check_online_payment',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def generate_payment_link(self, order_id, summ, email='', description=''):
        """
        @todo: todo
        :param order_id:
        :param summ:
        :param email:
        :param description:
        :return:
        """
        pass

    def generate_api_signature(self):
        """
        Generate api signature
        :return:str
        """
        return hashlib.md5(str(self.merchant_id).encode('utf-8') + str(self.second_secret).encode('utf-8')).hexdigest()

    def generate_wallet_signature(self):
        """
        Generate wallet signature
        :return:
        """
        return hashlib.md5(str(self.wallet_id + self.wallet_api_key).encode('utf-8')).hexdigest()
