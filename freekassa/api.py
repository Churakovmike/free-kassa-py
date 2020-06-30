import requests
import hashlib
from urllib.parse import urlencode


class FreeKassaApi:
    base_url = 'https://www.free-kassa.ru/api.php'
    base_form_url = 'http://www.free-kassa.ru/merchant/cash.php'
    base_export_order_url = 'https://www.free-kassa.ru/export.php'
    wallet_api_url = 'https://www.fkwallet.ru/api_v1.php'

    def __init__(self, merchant_id, first_secret,
                 second_secret, wallet_id, wallet_api_key=''):
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

    def export_order(self, status, date_from, date_to, limit=0, offset=100):
        """
        Get orders list.
        :param status:
        :param date_from:
        :param date_to:
        :param limit:
        :param offset:
        :return:
        """
        params = {
            'merchant_id': self.merchant_id,
            's': self.generate_api_signature(),
            'action': 'get_orders',
            'date_from': date_from,
            'date_to': date_to,
            'status': status,
            'limit': limit,
            'offset': offset,
        }

        return self.send_request(params=params)

    def withdraw(self, amount, currency):
        """
        Withdraw money.
        :param amount:
        :param currency:
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
        Create invoice.
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
        Get wallet balance.
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': self.generate_wallet_signature(),
            'action': self.get_balance(),
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def wallet_withdraw(self, purse, amount, currency,
                        description, disable_exchange=1):
        """
        Withdraw money from wallet.
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
            'action': 'cashout',
            'sign': self.__make_hash(params=[
                self.wallet_id,
                currency,
                amount,
                purse,
                self.wallet_api_key
            ]),
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_operation_status(self, payment_id):
        """
        Get operation status.
        :param payment_id:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'payment_id': payment_id,
            'sign': self.__make_hash(params=[
                self.wallet_id,
                payment_id,
                self.wallet_api_key
            ]),
            'action': 'get_payment_status',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def transfer_money(self, purse, amount):
        """
        Transfer money to another wallet.
        :param purse:
        :param amount:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'purse': purse,
            'amount': amount,
            'sign': self.__make_hash(params=[
                self.wallet_id,
                purse,
                amount,
                self.wallet_api_key
            ]),
            'action': 'transfer',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def online_payments(self, service_id, account, amount):
        """
        Payment online services.
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
            'sign': self.__make_hash(params=[
                self.wallet_id,
                amount,
                account,
                self.wallet_api_key
            ]),
            'action': 'online_payment',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_online_services(self):
        """
        Get list of payment services.
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': self.generate_wallet_signature(),
            'action': 'providers',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_online_payment_status(self, payment_id):
        """
        Check status online payment.
        :param payment_id:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'payment_id': payment_id,
            'sign': self.__make_hash(params=[
                self.wallet_id,
                payment_id,
                self.wallet_api_key
            ]),
            'action': 'check_online_payment',
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def create_btc_address(self):
        """
        Create BTC address.
        :return:
        """
        return self.create_crypto_address('create_btc_address')

    def create_ltc_address(self):
        """
        Create LTC address.
        :return:
        """
        return self.create_crypto_address('create_ltc_address')

    def create_eth_address(self):
        """
        Create ETH address.
        :return:
        """
        return self.create_crypto_address('create_eth_address')

    def create_crypto_address(self, action):
        """
        Create crypto wallet address.
        :param action:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': self.generate_wallet_signature(),
            'action': action,
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_btc_address(self):
        """
        Get BTC address.
        :return:
        """
        return self.get_crypto_address('get_btc_address')

    def get_ltc_address(self):
        """
        Get LTC address.
        :return:
        """
        return self.get_crypto_address('get_ltc_address')

    def get_eth_address(self):
        """
        GET ETH address.
        :return:
        """
        return self.get_crypto_address('get_eth_address')

    def get_crypto_address(self, action):
        """
        Get crypto address by action.
        :param action:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'sign': self.generate_wallet_signature(),
            'action': action,
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def get_btc_transaction(self, transaction_id):
        """
        Get information about BTC transaction.
        :param transaction_id:
        :return:
        """
        return self.get_transaction('get_btc_transaction', transaction_id)

    def get_ltc_transaction(self, transaction_id):
        """
        Get information about LTC transaction.
        :param transaction_id:
        :return:
        """
        return self.get_transaction('get_ltc_transaction', transaction_id)

    def get_eth_transaction(self, transaction_id):
        """
        Get information about ETH transaction.
        :param transaction_id:
        :return:
        """
        return self.get_transaction('get_eth_transaction', transaction_id)

    def get_transaction(self, action, transaction_id):
        """
        Get information about transaction by action.
        :param action:
        :param transaction_id:
        :return:
        """
        params = {
            'wallet_id': self.wallet_id,
            'transaction_id': transaction_id,
            'sign': self.__make_hash(params=[
                self.wallet_id,
                transaction_id,
                self.wallet_api_key
            ]),
            'action': action,
        }

        return self.send_request(params=params, url=self.wallet_api_url)

    def generate_payment_link(self, order_id, summ,
                              email='', description='') -> str:
        """
        Generate payment link for redirect user to Free-Kassa.com.
        :param order_id:
        :param summ:
        :param email:
        :param description:
        :return:
        """
        params = {
            'o': order_id,
            'oa': summ,
            's': self.generate_form_signature(summ, order_id),
            'm': self.merchant_id,
            'i': 'rub',
            'em': email,
            'lang': 'ru',
            'us_desc': description,
        }

        return self.base_form_url + "?" + urlencode(params)

    def generate_api_signature(self):
        """
        Generate api signature
        :return:str
        """
        return hashlib.md5(
            str(self.merchant_id).encode('utf-8')
            + str(self.second_secret).encode('utf-8')).hexdigest()

    def generate_wallet_signature(self):
        """
        Generate wallet signature
        :return:
        """
        return hashlib.md5(
            str(self.wallet_id + self.wallet_api_key).encode('utf-8'))\
            .hexdigest()

    def generate_form_signature(self, amount, order_id):
        """
        Generate signature for form and link
        :param amount:
        :param order_id:
        :return:
        """
        return self.__make_hash(sep=":", params=[
            str(self.merchant_id),
            str(amount),
            str(self.first_secret),
            str(order_id),
        ])

    def __make_hash(self, params, sep=' '):
        """
        Generate hash query for request params
        :param params:
        :param sep:
        :param args:
        :param kwargs:
        :return:
        """
        sign = f'{sep}'.join(params)
        return hashlib.md5(sign.encode('utf-8')).hexdigest()
