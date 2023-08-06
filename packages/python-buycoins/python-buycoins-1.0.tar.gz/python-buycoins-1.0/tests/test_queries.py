from unittest.mock import Mock

from . import responses
from buycoins import Query
from buycoins.utils import allowed_currencies


class TestQueries:
    Query = Mock()

    def test_get_balances(self):
        self.Query.get_balances.return_value = responses.get_balances
        balances = self.Query.get_balances()

        assert "getBalances" in balances["data"]
        assert len(balances["data"]["getBalances"]) == 6
        for currency in balances["data"]["getBalances"]:
            assert currency["cryptocurrency"] in allowed_currencies

    def test_get_specific_balance(self):
        self.Query.get_balances.return_value = responses.get_balance
        balance = self.Query.get_balances(cryptocurrency="bitcoin")

        assert "getBalances" in balance["data"]
        assert balance["data"]["getBalances"][0]["id"] == "QWNjb3VudC0="
        assert balance["data"]["getBalances"][0]["confirmedBalance"] == "0.0"
        assert balance["data"]["getBalances"][0]["cryptocurrency"] == "bitcoin"

    def test_get_bank_accounts(self):
        self.Query.get_bank_accounts.return_value = responses.get_bank_accounts
        bank_accounts = self.Query.get_bank_accounts()

        assert "getBankAccounts" in bank_accounts["data"]
        assert (
            bank_accounts["data"]["getBankAccounts"][0]["id"]
            == "QmFua0FjY291bnQtNjlkZGM2MjEtYzM0My00Mzg1LTlkMDYtY2VkNTM2MWY1Yjkz"
        )
        assert (
            bank_accounts["data"]["getBankAccounts"][0]["bankName"]
            == "ALAT by WEMA"
        )
        assert (
            bank_accounts["data"]["getBankAccounts"][0]["accountName"]
            == "kolapo ayesebotan"
        )
        assert (
            bank_accounts["data"]["getBankAccounts"][0]["accountNumber"]
            == "0235959654"
        )
        assert (
            bank_accounts["data"]["getBankAccounts"][0]["accountType"]
            == "withdrawal"
        )

    def test_get_specific_bank_account(self):
        self.Query.get_bank_accounts.return_value = responses.get_bank_accounts
        bank_account = self.Query.get_bank_accounts(account_number="0235959654")

        assert "getBankAccounts" in bank_account["data"]
        assert (
            bank_account["data"]["getBankAccounts"][0]["id"]
            == "QmFua0FjY291bnQtNjlkZGM2MjEtYzM0My00Mzg1LTlkMDYtY2VkNTM2MWY1Yjkz"
        )
        assert (
            bank_account["data"]["getBankAccounts"][0]["bankName"]
            == "ALAT by WEMA"
        )
        assert (
            bank_account["data"]["getBankAccounts"][0]["accountName"]
            == "kolapo ayesebotan"
        )
        assert (
            bank_account["data"]["getBankAccounts"][0]["accountNumber"]
            == "0235959654"
        )
        assert (
            bank_account["data"]["getBankAccounts"][0]["accountType"]
            == "withdrawal"
        )

    def test_get_estimated_network_fee_default(self):
        self.Query.get_estimated_network_fee.return_value = (
            responses.get_estimated_network_fee_default
        )
        network_fee = self.Query.get_estimated_network_fee(
            0.03
        )  # Bitcoin is implied by default

        assert "getEstimatedNetworkFee" in network_fee["data"]
        assert (
            network_fee["data"]["getEstimatedNetworkFee"]["total"] == "0.03036"
        )
        assert (
            network_fee["data"]["getEstimatedNetworkFee"]["estimatedFee"]
            == "0.00036"
        )

    def test_get_estimated_network_fee_ethereum(self):
        self.Query.get_estimated_network_fee.return_value = (
            responses.get_estimated_network_fee_ethereum
        )
        network_fee = self.Query.get_estimated_network_fee(
            0.03, cryptocurrency="ethereum"
        )

        assert "getEstimatedNetworkFee" in network_fee["data"]
        assert network_fee["data"]["getEstimatedNetworkFee"]["total"] == "0.04"
        assert (
            network_fee["data"]["getEstimatedNetworkFee"]["estimatedFee"]
            == "0.01"
        )

    def test_get_market_book_default(self):
        self.Query.get_market_book.return_value = responses.get_market_book_default
        market_book = self.Query.get_market_book() # Bitcoin is implied by default

        buy_node = market_book["data"]["getMarketBook"]["orders"]["edges"][0]["node"]
        sell_node = market_book["data"]["getMarketBook"]["orders"]["edges"][1]["node"]

        assert len(market_book["data"]["getMarketBook"]["orders"]["edges"]) == 2
        assert buy_node["id"] == "UG9zdE9yZGVyLTcxY2JmZjAxLTk2NTEtNGQzOC1hMGIyLWE2YzRkMDUzNWVkMA=="
        assert buy_node["cryptocurrency"] == "bitcoin"
        assert buy_node["coinAmount"] == "0.013797"
        assert buy_node["side"] == "buy"
        assert buy_node["status"] == "active"
        assert buy_node["createdAt"] == 1612808624
        assert buy_node["pricePerCoin"] == "19501000.0"
        assert buy_node["priceType"] == "static"
        assert buy_node["staticPrice"] == "1950100000"

        assert sell_node["id"] == "UG9zdE9yZGVyLTM5ODg2ZTNlLTJmZDQtNDgxNy05ODRjLWNlMTFlYmIwMzhlMw=="
        assert sell_node["cryptocurrency"] == "bitcoin"
        assert sell_node["coinAmount"] == "0.00653659"
        assert sell_node["side"] == "sell"
        assert sell_node["status"] == "active"
        assert sell_node["createdAt"] == 1612800454
        assert sell_node["pricePerCoin"] == "20500000.0"
        assert sell_node["priceType"] == "static"
        assert sell_node["staticPrice"] == "2050000000"

    def test_get_market_book_usd_tether(self):
        self.Query.get_market_book.return_value = responses.get_market_book_usd_tether
        market_book = self.Query.get_market_book(cryptocurrency="usd_tether")

        buy_node = market_book["data"]["getMarketBook"]["orders"]["edges"][0]["node"]
        sell_node = market_book["data"]["getMarketBook"]["orders"]["edges"][1]["node"]

        assert len(market_book["data"]["getMarketBook"]["orders"]["edges"]) == 2
        assert buy_node["id"] == "UG9zdE9yZGVyLWZmYTliOTdiLThmZjUtNDE4Mi05ZDJjLWM4ZWM5MzNlMTliZg=="
        assert buy_node["cryptocurrency"] == "usd_tether"
        assert buy_node["coinAmount"] == "100.0"
        assert buy_node["side"] == "buy"
        assert buy_node["status"] == "active"
        assert buy_node["createdAt"] == 1611770385
        assert buy_node["pricePerCoin"] == "460.0"
        assert buy_node["priceType"] == "static"
        assert buy_node["staticPrice"] == "46000"

        assert sell_node["id"] == "UG9zdE9yZGVyLWI5ZWJkYWNmLTQ1MjYtNDYxYS1hYzFlLTljZTZlNTRmOWFkOA=="
        assert sell_node["cryptocurrency"] == "usd_tether"
        assert sell_node["coinAmount"] == "234.0"
        assert sell_node["side"] == "sell"
        assert sell_node["status"] == "active"
        assert sell_node["createdAt"] == 1612413166
        assert sell_node["pricePerCoin"] == "499.0"
        assert sell_node["priceType"] == "static"
        assert sell_node["staticPrice"] == "49900"

    def test_get_orders(self):
        self.Query.get_orders.return_value = responses.get_orders
        orders = self.Query.get_orders("open")

        node = orders["data"]["getOrders"]["orders"]["edges"][0]["node"]

        assert node["id"] == "UG9zdE9yZGVyLWEzYTAwNzQxLTJhMWUtNGJkMi1iZWFkLWE2ZWU0MzQ1ZmI2Yw=="
        assert node["cryptocurrency"] == "bitcoin"
        assert node["coinAmount"] == "0.005"
        assert node["side"] == "buy"
        assert node["status"] == "active"
        assert node["createdAt"] == 1605000847
        assert node["pricePerCoin"] == "10900.09"
        assert node["priceType"] == "static"
        assert node["staticPrice"] == "1090009"

    def test_get_payments(self):
        self.Query.get_payments.return_value = responses.get_payments
        payments = self.Query.get_payments()

        node = payments["data"]["getPayments"]["edges"][0]["node"]

        assert node["id"] == "UG9zdE9yZGVyLTg5MDM4MzI4LTc5MzItNGUxMS1hZWZjLTkwYjg4ZTFhY2JjOA=="
        assert node["fee"] == "0.0046"
        assert node["amount"] == "10000.00"
        assert node["createdAt"] == 1605000847
        assert node["reference"] == "38d5d9018bde98e88058746788d72e936d158f5ad753073f4763dc1d4aa5a48e"
        assert node["status"] == "success"
        assert node["totalAmount"] == "10000.004600"
        assert node["type"] == "deposit"

    def test_get_prices(self):
        self.Query.get_prices.return_value = responses.get_prices
        prices = self.Query.get_prices()

        assert len(prices["data"]["getPrices"]) == 4
        for price in prices["data"]["getPrices"]:
            assert price["cryptocurrency"] in allowed_currencies

        bitcoin_price = prices["data"]["getPrices"][0]
        assert bitcoin_price["id"] == "QnV5Y29pbnNQcmljZS01OTkwYTQ0NC1hYjY4LTQxM2MtODUzZC04OWJhYzRhMWNjZjE="
        assert bitcoin_price["status"] == "active"
        assert bitcoin_price["cryptocurrency"] == "bitcoin"
        assert bitcoin_price["minBuy"] == "0.001"
        assert bitcoin_price["minSell"] == "0.001"
        assert bitcoin_price["maxBuy"] == "1.78700697"
        assert bitcoin_price["maxSell"] == "1.20119207"
        assert bitcoin_price["minCoinAmount"] == "0.001"
        assert bitcoin_price["expiresAt"] == 1612847212
        assert bitcoin_price["buyPricePerCoin"] == "21956210.523"
        assert bitcoin_price["sellPricePerCoin"] == "21521388.24"

    def test_get_specific_price(self):
        self.Query.get_prices.return_value = responses.get_price
        prices = self.Query.get_prices(cryptocurrency="ethereum")

        eth_price = prices["data"]["getPrices"][0]
        assert eth_price["id"] == "QnV5Y29pbnNQcmljZS0yOWFmZWY4MS1mZjI5LTQwYTQtYmQ3Zi1iOTgzMTA3NmU5NDg="
        assert eth_price["status"] == "active"
        assert eth_price["cryptocurrency"] == "ethereum"
        assert eth_price["minBuy"] == "0.02"
        assert eth_price["minSell"] == "0.02"
        assert eth_price["maxBuy"] == "48.07685652"
        assert eth_price["maxSell"] == "0"
        assert eth_price["minCoinAmount"] == "0.02"
        assert eth_price["expiresAt"] == 1612847332
        assert eth_price["buyPricePerCoin"] == "816107.8759"
        assert eth_price["sellPricePerCoin"] == "799786.8945"
