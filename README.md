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
```python
from freekassa import FreeKassaApi

client = FreeKassaApi(
    first_secret='first_secret_key',
    second_secret='second_secret_key',
    merchant_id='merchant_id',
    wallet_id='wallet_id')

balance = client.get_balance()
```
