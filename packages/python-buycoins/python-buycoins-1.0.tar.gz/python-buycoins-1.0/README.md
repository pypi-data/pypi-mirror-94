# BuyCoins API library
A Python module for interacting with buyCoins API. [See official documentation](https://developers.buycoins.africa/)
## Getting started
Installation via Pip:
```sh
$ pip install python-buycoins
```

This module consists of a Query class and a Mutation class. The Query class contains all queries in the API while the Mutation class
contains all mutations in the API.

The Query class has the following methods:
 - get_bank_accounts()
 - get_balances()
 - get_estimated_network_fee()
 - get_market_book()
 - get_orders()
 - get_payments()
 - get_prices()

...and the Mutation class has the following:
 - buy()
 - cancel_withdrawal()
 - create_address()
 - create_deposit_account()
 - create_withdrawal()
 - post_limit_order()
 - post_market_order()
 - sell()
 - send()
 - send_off_chain()

## Authentication
You should place `PUBLIC_KEY` and `PRIVATE_KEY` in your .env file as seen in `.env.example`  

## Usage
```python
from buycoins import Executor, Query, Mutation

# Instantiate the classes:
que = Query()
mut = Mutation()

# Example queries
data = que.get_balances() # get balances
data = que.get_bank_accounts() # get account details

# Example mutations
data = mut.buy(0.03) # buy 0.03 worth of bitcoin
data = mut.create_address() # create a bitcoin address to receive

# Wanna execute your own queries? Use the Executor() class
# If PUBLIC_KEY and PRIVATE_KEY is already in .env, do this:
exe = Executor()
# Else:
exe = Executor(PUBLIC_KEY, PRIVATE_KEY)

data = exe.query(query_str, variables)

```

All methods have an optional `query` argument. You need not worry about passing this argument because by the default value is sufficient and returns all fields. All query strings are defined in the `constants.py` file.

## Method Signature
### Queries

##### ```get_balances(self, cryptocurrency=None, query=GET_BALANCES)```
Retrieve supported cryptocurrencies account balance.\
Valid **cryptocurrency** values are: *usd_tether*, *naira_token*, *bitcoin*, *ethereum*, *litecoin*, *usd_coin*.
##### ```get_bank_accounts(self, account_number=None, query=GET_BANK_ACCOUNTS)```
Retrieve bank accounts.
##### ```get_estimated_network_fee(self, amount, cryptocurrency="bitcoin", query=GET_ESTIMATED_NETWORK_FEE)```
Retrieve estimated network fee to send supported cryptocurrencies.
##### ```get_market_book(self, coin_amount=None, cryptocurrency="bitcoin", query=GET_MARKET_BOOK)```
Retrieve a list of orders on the peer-to-peer (P2P) platform.
##### ```get_orders(self, status, side=None, cryptocurrency="bitcoin", query=GET_ORDERS)```
Retrieve a list of orders.\
**side** takes either *buy* or *sell*.\
**status** takes either *open* or *completed*.
##### ```get_payments(self, query=GET_PAYMENTS)```
Retrieve a list of payments.
##### ```get_prices(self, side=None, cryptocurrency=None, query=GET_PRICES)```
Retrieve buy/sell price(s) for supported cryptocurrencies.

### Mutations

##### ```buy(self, coin_amount, price=None, cryptocurrency="bitcoin", query=BUY)```
Buy supported cryptocurrencies. If *price* is not specified, it fetches an active price internally.
##### ```cancel_withdrawal(self, payment, query=CANCEL_WITHDRAWAL)```
Cancel initiated withdrawal. The ID of the payment to be cancelled should be passed in as the *payment* parameter.
##### ```create_address(self, cryptocurrency="bitcoin", query=CREATE_ADDRESS)```
Create address to receive supported cryptocurrencies.
##### ```create_deposit_account(self, account_name, query=CREATE_DEPOSIT_ACCOUNT)```
Generate deposit bank accounts to top up your NGNT account with Naira.
##### ```create_withdrawal(self, amount, account_id=None, account_number=None, query=CREATE_WITHDRAWAL)```
Create a new withdrawal. This requires the ID of the bank to withdraw to. You can easily get that using *get_bank_accounts()*. Whatever ID obtained from calling *get_bank_accounts()* should be specified as *account_id*. However, this method allows you to specify an account number (specified as value to *account_number*) and the account ID will be fetched internally. If you specify both *account_id* and *account_number*, an exception is thrown. 
##### ```post_limit_order(self, order_side, coin_amount, price_type, cryptocurrency="bitcoin", static_price=None, dynamic_exchange_rate=None, query=POST_LIMIT_ORDER)```
Create a new limit order.\
**order_side** should be either *buy* or *sell*\
**price_type** should be either *static* or *dynamic*\
**static_price** and **dynamic_exchange_rate** depends on the value of **price_type**. If price_type is *static*, then static_price is required. If price_type is dynamic, dynamic_exchange_rate is required.
##### ```post_market_order(self, order_side, coin_amount, cryptocurrency="bitcoin", query=POST_MARKET_ORDER)```
Create a new market order.
##### ```sell(self, coin_amount, price=None, cryptocurrency="bitcoin", query=SELL)```
Sell supported cryptocurrencies. If *price* is not specified, it fetches an active price internally.
##### ```send(self, amount, address, cryptocurrency="bitcoin", query=SEND)```
Send supported cryptocurrencies to external address.
##### ```send_off_chain(self, amount, recipient, cryptocurrency="bitcoin", query=SEND_OFF_CHAIN)```
Send supported cryptocurrencies to internal BuyCoins users.

## Running tests
To run tests, do:
```sh
pytest -sv
```

## License
(c) 2021 Immanuel Kolapo

This repository is licensed under the MIT license. See LICENSE for details.
