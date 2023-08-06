from typing import Dict, Any

from .constants import (
    BUY,
    CANCEL_WITHDRAWAL,
    CREATE_ADDRESS,
    CREATE_DEPOSIT_ACCOUNT,
    CREATE_WITHDRAWAL,
    POST_LIMIT_ORDER,
    POST_MARKET_ORDER,
    SELL,
    SEND,
    SEND_OFF_CHAIN,
)
from .queries import Query
from .executor import Executor
from .utils import validator


class Mutation(Executor):
    """This class holds together all mutations in the Buycoins API."""

    q = Query()

    def buy(
        self,
        coin_amount: float,
        price: str = None,
        cryptocurrency: str = "bitcoin",
        query_str: str = BUY,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Buy supported cryptocurrencies.
        If `price` is not specified, it fetches an active
        price internally.

        Parameters
        ----------
        coin_amount : float
            The amount involved in the transaction.
        price : str, optional
            The ID of the active price. Provided if not
            supplied.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is BUY).

        Returns
        -------
        results : dict
            A dictionary containing details of the buy order.
        """

        _ = validator(currency=cryptocurrency)

        if not price:
            price_data = self.q.get_prices("buy", cryptocurrency=cryptocurrency)
            price = price_data["data"]["getPrices"][0]["id"]

        variables = {
            "cryptocurrency": cryptocurrency,
            "coin_amount": coin_amount,
            "price": price,
        }
        results = self.query(query_str, variables)

        return results

    def cancel_withdrawal(
        self, payment: str, query_str: str = CANCEL_WITHDRAWAL
    ) -> Dict[str, Dict[str, Any]]:

        """
        Cancel initiated withdrawal.

        Parameters
        ----------
        payment : str
            The ID of the payment to be cancelled.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is CANCEL_WITHDRAWAL).

        Returns
        -------
        results : dict
            A dictionary containing details of the payment.
        """

        variables = {"payment": payment}
        results = self.query(query_str, variables)

        return results

    def create_address(
        self, cryptocurrency: str = "bitcoin", query_str: str = CREATE_ADDRESS
    ) -> Dict[str, Dict[str, Any]]:

        """
        Create address to receive supported cryptocurrencies.

        Parameters
        ----------
        cryptocurrency : str, optional
            The cryptocurrency for which the address is to be generated
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is CREATE_ADDRESS).

        Returns
        -------
        results : dict
            A dictionary containing address details.
        """

        _ = validator(currency=cryptocurrency)

        variables = {"cryptocurrency": cryptocurrency}
        results = self.query(query_str, variables)

        return results

    def create_deposit_account(
        self, account_name: str, query_str: str = CREATE_DEPOSIT_ACCOUNT
    ) -> Dict[str, Dict[str, Any]]:

        """
        Generate deposit bank accounts to top up your NGNT
        account with Naira.

        Parameters
        ----------
        account_name : str
            The full name of the account holder.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is CREATE_DEPOSIT_ACCOUNT).

        Returns
        -------
        results : dict
            A dictionary containing generated account details.
        """

        variables = {"accountName": account_name}
        results = self.query(query_str, variables)

        return results

    def create_withdrawal(
        self,
        amount: float,
        account_id: str = None,
        account_number: str = None,
        query_str: str = CREATE_WITHDRAWAL,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Create a new withdrawal.

        Parameters
        ----------
        amount : float
            The amount to be withdrawn.
        account_id : str, optional
            The ID of the account from which the withdrawal is to be made.
        account_number : str, optional
            The account number of the account from which the withdrawal is
            to be made.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is CREATE_WITHDRAWAL).

        Returns
        -------
        results : dict
            A dictionary containing details of the payment or withdrawal.
        """

        if account_id and account_number:
            raise ValueError(
                "You may only provide one of `account_id` or `account_number`!"
            )

        if account_id:
            bank_account = account_id
        elif account_number:
            bank_account_data = self.q.get_bank_accounts(account_number)
            if not bank_account_data["data"]["getBankAccounts"]:
                raise ValueError("Bank not found!")

            bank_account = bank_account_data["data"]["getBankAccounts"][0]["id"]

        variables = {"bankAccount": bank_account, "amount": amount}
        results = self.query(query_str, variables)

        return results

    def post_limit_order(
        self,
        order_side: str,
        coin_amount: float,
        price_type: str,
        cryptocurrency: str = "bitcoin",
        static_price: float = None,
        dynamic_exchange_rate: float = None,
        query_str: str = POST_LIMIT_ORDER,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Create a new limit order.

        Parameters
        ----------
        order_side : str
            The type of transaction - "buy" or "sell".
        coin_amount : float
            The amount involved in the transaction.
        price_type : str
            The price type - "static" or "dynamic".
        cryptocurrency : str, optional
            The cryptocurrency involved in the transaction
            (default is bitcoin).
        static_price: float, optional
            The static price in naira. Required if price_type
            is static.
        dynamic_exchange_rate: float, optional
            The dynamic exchange rate in naira. Required if price_type
            is dynamic.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is POST_LIMIT_ORDER).

        Returns
        -------
        results : dict
            A dictionary containing details of the market order.
        """

        _ = validator(
            side=order_side, price_type=price_type, currency=cryptocurrency
        )

        variables = {
            "orderSide": order_side,
            "coinAmount": coin_amount,
            "priceType": price_type,
            "cryptocurrency": cryptocurrency,
            "staticPrice": static_price,
            "dynamicExchangeRate": dynamic_exchange_rate,
        }
        results = self.query(query_str, variables)

        return results

    def post_market_order(
        self,
        order_side: str,
        coin_amount: str,
        cryptocurrency: str = "bitcoin",
        query_str: str = POST_MARKET_ORDER,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Create a new market order.

        Parameters
        ----------
        order_side : str
            The type of transaction - "buy" or "sell".
        coin_amount : float
            The amount involved in the transaction.
        cryptocurrency : str, optional
            The cryptocurrency involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is POST_MARKET_ORDER).

        Returns
        -------
        results : dict
            A dictionary containing details of the market order.
        """

        _ = validator(side=order_side, currency=cryptocurrency)

        variables = {
            "orderSide": order_side,
            "coinAmount": coin_amount,
            "cryptocurrency": cryptocurrency,
        }
        results = self.query(query_str, variables)

        return results

    def sell(
        self,
        coin_amount: float,
        price: str = None,
        cryptocurrency: str = "bitcoin",
        query_str: str = SELL,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Sell supported cryptocurrencies.
        If `price` is not specified, it fetches an active
        price internally.

        Parameters
        ----------
        coin_amount : float
            The amount involved in the transaction.
        price : str, optional
            The ID of the active price. Provided if not
            supplied.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is SELL).

        Returns
        -------
        results : dict
            A dictionary containing details of the sell order.
        """

        _ = validator(currency=cryptocurrency)

        if not price:
            price_data = self.q.get_prices(
                "sell", cryptocurrency=cryptocurrency
            )
            price = price_data["data"]["getPrices"][0]["id"]

        variables = {
            "cryptocurrency": cryptocurrency,
            "coin_amount": coin_amount,
            "price": price,
        }
        results = self.query(query_str, variables)

        return results

    def send(
        self,
        amount: float,
        address: str,
        cryptocurrency: str = "bitcoin",
        query_str: str = SEND,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Send supported cryptocurrencies to external address.

        Parameters
        ----------
        amount : float
            The amount to send.
        address : str
            The external address to send to.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is SEND).

        Returns
        -------
        results : dict
            A dictionary containing details of the onchain transfer.
        """

        _ = validator(currency=cryptocurrency)

        variables = {
            "amount": amount,
            "address": address,
            "cryptocurrency": cryptocurrency,
        }
        results = self.query(query_str, variables)

        return results

    def send_off_chain(
        self,
        amount: float,
        recipient: str,
        cryptocurrency: str = "bitcoin",
        query_str: str = SEND_OFF_CHAIN,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Send supported cryptocurrencies to internal BuyCoins users.

        Parameters
        ----------
        amount : float
            The amount to send.
        recipient : str
            The username of the recipient.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (Default
            is SEND_OFF_CHAIN).

        Returns
        -------
        results : dict
            A dictionary containing details of the initiated transfer.
        """

        _ = validator(currency=cryptocurrency)

        variables = {
            "amount": amount,
            "recipient": recipient,
            "cryptocurrency": cryptocurrency,
        }
        results = self.query(query_str, variables)

        return results
