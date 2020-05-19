FreeKassa API client
====================

Installation
-------------
Install this package with pip
```commandline
pip install free-kassa-py
```

Usage
-----
#### Check balance
```python
from freekassa import FreeKassaApi

client = FreeKassaApi(
    first_secret='first_secret_key',
    second_secret='second_secret_key',
    merchant_id='merchant_id',
    wallet_id='wallet_id')

balance = client.get_balance()
```

#### Check order
```python
order = client.get_order(order_id, int_id)
```

#### Generate payment link
```python
payment_link = client.generate_payment_link(order_id, summ, email, description)
```

#### Export orders to xml
```python
data = client.export_order(status, date_from, date_to, limit, offest)
```

#### Withdraw money
```python
withdraw = client.withdraw(amount, currency)
```

#### Invoicing
```python
invoice = client.invoice(email, amount, description)
```

#### Get wallet balance
```python
wallet_balance = client.get_wallet_balance()
```

#### Withdraw money from wallet
```python
wallet_withdraw = client.wallet_withdraw(purse, amount, currency, description, disable_exchange)
```

#### Get wallet operation status
```python
operation_status = client.get_operation_status(payment_id)
```

#### Transfer money to another wallet
```python
transfer = client.transfer_money(purse, amount)
```

#### Payment for online services
```python
payment = client.online_payments(ervice_id, account, amount)
```

#### Get list of services for online payment
```python
services = client.get_online_services()
```

#### Check status online payment
```python
payment_status = client.get_online_payment_status(payment_id)
```

#### Create crypto wallet address
```python
btc_wallet = client.create_btc_address()
ltc_wallet = client.create_ltc_address()
eth_wallet = client.create_eth_address()
```

### Get crypto wallet address
```python
btc_wallet_address = client.get_btc_address()
ltc_wallet_address = client.get_ltc_address()
eth_wallet_address = client.get_eth_address()
```

#### Get information about transaction
```python
btc_transaction = client.get_btc_transaction(transaction_id)
ltc_transaction = client.get_ltc_transaction(transaction_id)
eth_transaction = client.get_eth_transaction(transaction_id)
```
