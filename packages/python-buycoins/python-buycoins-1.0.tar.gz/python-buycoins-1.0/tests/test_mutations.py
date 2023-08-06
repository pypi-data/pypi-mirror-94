from unittest.mock import Mock

from . import responses
from buycoins import Mutation


class TestMutations:
    Mutation = Mock()

    def test_buy_default(self):
        self.Mutation.buy.return_value = responses.buy_default
        buy = self.Mutation.buy(0.03)  # Bitcoin is implied

        assert "buy" in buy["data"]
        assert (
            buy["data"]["buy"]["id"]
            == "QnV5Y29pbnNQcmljZS11MENzAnJ31T2jNaBzMRR3ZaRuZkGkAD2lAUN3NkMiNUGjAnV="
        )
        assert (
            buy["data"]["buy"]["price"]
            == responses.get_prices["data"]["getPrices"][0]
        )
        assert buy["data"]["buy"]["cryptocurrency"] == "bitcoin"
        assert buy["data"]["buy"]["filledCoinAmount"] == "1.230000"
        assert buy["data"]["buy"]["side"] == "buy"
        assert buy["data"]["buy"]["status"] == "pending"
        assert buy["data"]["buy"]["totalCoinAmount"] == "0.03"
        assert buy["data"]["buy"]["createdAt"] == 1612847212

    def test_buy_ethereum(self):
        self.Mutation.buy.return_value = responses.buy_ethereum
        buy = self.Mutation.buy(1.3, cryptocurrency="ethereum")

        assert "buy" in buy["data"]
        assert (
            buy["data"]["buy"]["id"]
            == "QnV5Y29pbnNQcmljZS16iR364whgHoYiAMsKGpxJEWIZmOTjqz7OssziZyAbtnlSVC="
        )
        assert (
            buy["data"]["buy"]["price"]
            == responses.get_prices["data"]["getPrices"][1]
        )
        assert buy["data"]["buy"]["cryptocurrency"] == "ethereum"
        assert buy["data"]["buy"]["filledCoinAmount"] == "3.223432"
        assert buy["data"]["buy"]["side"] == "buy"
        assert buy["data"]["buy"]["status"] == "done"
        assert buy["data"]["buy"]["totalCoinAmount"] == "1.3"
        assert buy["data"]["buy"]["createdAt"] == 1612847212

    def test_cancel_withdrawal(self):
        self.Mutation.cancel_withdrawal.return_value = (
            responses.cancel_withdrawal
        )
        withdrawal = self.Mutation.cancel_withdrawal(
            "QWRkcmVzcy1hz8V54ffgpB2pX52m8IG2fMgToM2ln5H3k3QJYNyShpz8EiF="
        )
        assert "cancelWithdrawal" in withdrawal["data"]
        assert (
            withdrawal["data"]["cancelWithdrawal"]["id"]
            == "QWRkcmVzcy1hz8V54ffgpB2pX52m8IG2fMgToM2ln5H3k3QJYNyShpz8EiF="
        )
        assert withdrawal["data"]["cancelWithdrawal"]["fee"] == "0.046"
        assert withdrawal["data"]["cancelWithdrawal"]["createdAt"] == 1612847212
        assert (
            withdrawal["data"]["cancelWithdrawal"]["reference"]
            == "zmJxqDM3-dz_sPoi7LwalRM5N8Q711BllncBuq476xw"
        )
        assert withdrawal["data"]["cancelWithdrawal"]["status"] == "pending"
        assert (
            withdrawal["data"]["cancelWithdrawal"]["totalAmount"]
            == "100000.046"
        )
        assert withdrawal["data"]["cancelWithdrawal"]["type"] == "withdrawal"

    def test_create_address_default(self):
        self.Mutation.create_address.return_value = (
            responses.create_address_default
        )
        address = self.Mutation.create_address()  # Bitcoin is implied

        assert "createAddress" in address["data"]
        assert (
            address["data"]["createAddress"]["id"]
            == "QWRkcmVzcy1hMWU2YTRlMy1iOTBhLTQwMWEtOWNkZS00OTM5NWZlOWIzZWY="
        )
        assert (
            address["data"]["createAddress"]["address"]
            == "39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8"
        )
        assert address["data"]["createAddress"]["cryptocurrency"] == "bitcoin"
        assert address["data"]["createAddress"]["createdAt"] == 1612857009

    def test_create_address_ethereum(self):
        self.Mutation.create_address.return_value = (
            responses.create_address_ethereum
        )
        address = self.Mutation.create_address(cryptocurrency="ethereum")

        assert "createAddress" in address["data"]
        assert (
            address["data"]["createAddress"]["id"]
            == "QWRkcmVzcy05NmQyZDdmNS05NDgxLTQwODMtODdlOC01ZjdmM2QwODZiYzg="
        )
        assert (
            address["data"]["createAddress"]["address"]
            == "0x64b82318cadaf1209b16726d5634455762748a90"
        )
        assert address["data"]["createAddress"]["cryptocurrency"] == "ethereum"
        assert address["data"]["createAddress"]["createdAt"] == 1612857154

    def test_create_deposit_account(self):
        self.Mutation.create_deposit_account.return_value = (
            responses.create_deposit_account
        )
        account = self.Mutation.create_deposit_account(
            account_name="Dummy User"
        )

        assert "createDepositAccount" in account["data"]
        assert (
            account["data"]["createDepositAccount"]["id"]
            == "QmFua0FjY291bnTffyORgTFvah6zcxBllmkbEcJb6gQigoWKwbl6yCP2MWY1Yjkz"
        )
        assert (
            account["data"]["createDepositAccount"]["bankName"]
            == "Providus Bank"
        )
        assert (
            account["data"]["createDepositAccount"]["accountName"]
            == "Dummy User"
        )
        assert (
            account["data"]["createDepositAccount"]["accountNumber"]
            == "9008007000"
        )
        assert (
            account["data"]["createDepositAccount"]["accountType"] == "deposit"
        )
        assert (
            account["data"]["createDepositAccount"]["accountReference"]
            == "3T3B_3TM9kuf-rBenmSvN-RL"
        )

    def test_create_withdrawal(self):
        self.Mutation.create_withdrawal.return_value = (
            responses.create_withdrawal
        )
        withdrawal = self.Mutation.create_withdrawal(
            10000,
            account_id=responses.get_bank_accounts["data"]["getBankAccounts"][
                0
            ]["id"],
        )

        assert "createWithdrawal" in withdrawal["data"]
        assert (
            withdrawal["data"]["createWithdrawal"]["id"]
            == "QWRkcmVzcy1hz8V5vMlQ1f4Kk9MUziKwKdtiOAll2qPRpdve6S4wWaUBeYk="
        )
        assert withdrawal["data"]["createWithdrawal"]["fee"] == "0.046"
        assert withdrawal["data"]["createWithdrawal"]["amount"] == "100000.00"
        assert withdrawal["data"]["createWithdrawal"]["createdAt"] == 1612867302
        assert (
            withdrawal["data"]["createWithdrawal"]["reference"]
            == "hPm000GJBexlW2cfeYsalonCwTxzSXNwh-QoAEv_A8s"
        )
        assert withdrawal["data"]["createWithdrawal"]["status"] == "pending"
        assert (
            withdrawal["data"]["createWithdrawal"]["totalAmount"]
            == "100000.046"
        )
        assert withdrawal["data"]["createWithdrawal"]["type"] == "withdrawal"

    def test_post_limit_order(self):
        self.Mutation.post_limit_order.return_value = responses.post_limit_order
        limit_order = self.Mutation.post_limit_order(
            "buy", 0.00819931, "static", static_price=2205000000
        )  # Bitcoin is implied

        assert "postLimitOrder" in limit_order["data"]
        assert (
            limit_order["data"]["postLimitOrder"]["id"]
            == "UG9zdE9yZGVyLWYyNGMzNmVlLTAwZmMtNGM1Ny04MmJkLWYzOGI4ZTA0MTAxMw=="
        )
        assert (
            limit_order["data"]["postLimitOrder"]["cryptocurrency"] == "bitcoin"
        )
        assert (
            limit_order["data"]["postLimitOrder"]["coinAmount"] == "0.00819931"
        )
        assert limit_order["data"]["postLimitOrder"]["side"] == "buy"
        assert limit_order["data"]["postLimitOrder"]["status"] == "inactive"
        assert limit_order["data"]["postLimitOrder"]["createdAt"] == 1612867863
        assert (
            limit_order["data"]["postLimitOrder"]["pricePerCoin"]
            == "2205000000.0"
        )
        assert limit_order["data"]["postLimitOrder"]["priceType"] == "static"
        assert (
            limit_order["data"]["postLimitOrder"]["staticPrice"]
            == "220500000000"
        )

    def test_post_market_order(self):
        self.Mutation.post_market_order.return_value = (
            responses.post_market_order
        )
        market_order = self.Mutation.post_market_order(
            "sell", 0.0004
        )  # Bitcoin is implied

        assert "postMarketOrder" in market_order["data"]
        assert (
            market_order["data"]["postMarketOrder"]["id"]
            == "UG9zdE9yZGVyLWYyNGMzHMGTaSx0XuVMIiI7qXyRnZ7MzuooxOApisAuIov3k8=="
        )
        assert (
            market_order["data"]["postMarketOrder"]["cryptocurrency"]
            == "bitcoin"
        )
        assert market_order["data"]["postMarketOrder"]["coinAmount"] == "0.0004"
        assert market_order["data"]["postMarketOrder"]["side"] == "sell"
        assert market_order["data"]["postMarketOrder"]["status"] == "active"
        assert (
            market_order["data"]["postMarketOrder"]["createdAt"] == 1612867873
        )
        assert (
            market_order["data"]["postMarketOrder"]["pricePerCoin"]
            == "2205000000.0"
        )
        assert market_order["data"]["postMarketOrder"]["priceType"] == "static"
        assert (
            market_order["data"]["postMarketOrder"]["staticPrice"]
            == "220500000000"
        )

    def test_sell_default(self):
        self.Mutation.sell.return_value = responses.sell_default
        sell = self.Mutation.sell(0.03)  # Bitcoin is implied

        assert "sell" in sell["data"]
        assert (
            sell["data"]["sell"]["id"]
            == "QnV5Y29pbnNQcmljZS11KSkCEauCpTyq3vbbW6TKrjIfwfvjcVJYvomfKOtJTRwjAnV="
        )
        assert (
            sell["data"]["sell"]["price"]
            == responses.get_prices["data"]["getPrices"][0]
        )
        assert sell["data"]["sell"]["cryptocurrency"] == "bitcoin"
        assert sell["data"]["sell"]["filledCoinAmount"] == "1.230000"
        assert sell["data"]["sell"]["side"] == "sell"
        assert sell["data"]["sell"]["status"] == "pending"
        assert sell["data"]["sell"]["totalCoinAmount"] == "0.03"
        assert sell["data"]["sell"]["createdAt"] == 1612847212

    def test_sell_ethereum(self):
        self.Mutation.sell.return_value = responses.sell_ethereum
        sell = self.Mutation.sell(1.3, cryptocurrency="ethereum")

        assert "sell" in sell["data"]
        assert (
            sell["data"]["sell"]["id"]
            == "QnV5Y29pbnNQcmljZS16CZ3R79tuZUJFTSCaWzqnMKe0a17EWh35i1WZhdW5Mg8SVC="
        )
        assert (
            sell["data"]["sell"]["price"]
            == responses.get_prices["data"]["getPrices"][1]
        )
        assert sell["data"]["sell"]["cryptocurrency"] == "ethereum"
        assert sell["data"]["sell"]["filledCoinAmount"] == "3.223432"
        assert sell["data"]["sell"]["side"] == "sell"
        assert sell["data"]["sell"]["status"] == "done"
        assert sell["data"]["sell"]["totalCoinAmount"] == "1.3"
        assert sell["data"]["sell"]["createdAt"] == 1612847212

    def test_send(self):
        self.Mutation.send.return_value = responses.send
        send = self.Mutation.send(
            0.03, address="39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8"
        )  # Bitcoin is implied

        assert "send" in send["data"]
        assert (
            send["data"]["send"]["id"]
            == "QnV5Y29pbnNQcmljZS16CZ3RctvVxtbTeS51jh1aQrmCZkxoMdKw8isRG89UbZovH4="
        )
        assert send["data"]["send"]["fee"] == "0.00024"
        assert send["data"]["send"]["amount"] == "0.2"
        assert (
            send["data"]["send"]["address"]
            == "39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8"
        )
        assert send["data"]["send"]["cryptocurrency"] == "bitcoin"
        assert send["data"]["send"]["status"] == "processing"
        assert (
            send["data"]["send"]["transaction"]["txhash"]
            == "8223715e93f1c8715a8070b323acee111c1cadeb1eff16fe44b60e4269c175ab"
        )
        assert send["data"]["send"]["transaction"]["confirmed"] == False

    def test_send_off_chain(self):
        self.Mutation.send_off_chain.return_value = responses.send_off_chain
        send = self.Mutation.send_off_chain(0.03, "cimmanuel")  # Bitcoin is implied

        assert "sendOffchain" in send["data"]
        assert send["data"]["sendOffchain"]["initiated"] == True
