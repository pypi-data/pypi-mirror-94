from typing import Any, Dict, List, Optional

from .constants import (
    GET_BALANCES,
    GET_BANK_ACCOUNTS,
    GET_ESTIMATED_NETWORK_FEE,
    GET_MARKET_BOOK,
    GET_ORDERS,
    GET_PAYMENTS,
    GET_PRICES,
)
from .executor import Executor
from .utils import validator


class Query(Executor):
    """This class holds together all queries in the Buycoins API."""

    def get_balances(
        self, cryptocurrency: str = None, query_str: str = GET_BALANCES
    ) -> Dict[str, Dict[str, List[Dict[str, str]]]]:

        """
        Retrieve supported cryptocurrencies account balance.

        Parameters
        ----------
        cryptocurrency : str, optional
            The cryptocurrency which the balance is needed.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_BALANCES).

        Returns
        -------
        results : dict
            A dictionary containing the balance of the currency
            provided.
        """

        if cryptocurrency:
            _ = validator(currency=cryptocurrency)

        variables = {"cryptocurrency": cryptocurrency}
        results = self.query(query_str, variables)

        return results

    def get_bank_accounts(
        self, account_number: str = None, query_str: str = GET_BANK_ACCOUNTS
    ) -> Dict[str, Dict[str, List[Dict[str, Optional[str]]]]]:

        """
        Retrieve bank accounts.

        Parameters
        ----------
        account_number : str, optional
            The account number which the detail is to be retrieved.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_BANK_ACCOUNTS).

        Returns
        -------
        results : dict
            A dictionary containing details of the provided
            account number.
        """

        variables = {"accountNumber": account_number}
        results = self.query(query_str, variables)

        return results

    def get_estimated_network_fee(
        self,
        amount: float,
        cryptocurrency: str = "bitcoin",
        query_str: str = GET_ESTIMATED_NETWORK_FEE,
    ) -> Dict[str, Dict[str, Dict[str, str]]]:

        """
        Retrieve estimated network fee to send supported
        cryptocurrencies.

        Parameters
        ----------
        amount : float
            The amount involved in the transaction.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_ESTIMATED_NETWORK_FEE).

        Returns
        -------
        results : dict
            A dictionary containing the total amount
            (estimated fee + balance) and estimated fee for send.
        """

        _ = validator(currency=cryptocurrency)

        variables = {"cryptocurrency": cryptocurrency, "amount": amount}
        results = self.query(query_str, variables)

        return results

    def get_market_book(
        self,
        coin_amount: float = None,
        cryptocurrency: str = "bitcoin",
        query_str: str = GET_MARKET_BOOK,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Retrieve a list of orders on the P2P platform.

        Parameters
        ----------
        coin_amount : float
            The amount of coin involved in the transaction.
        cryptocurrency : str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_MARKET_BOOK).

        Returns
        -------
        results : dict
            A dictionary containing a list of orders on the P2P platform.
        """

        _ = validator(currency=cryptocurrency)

        variables = {
            "cryptocurrency": cryptocurrency,
            "coinAmount": coin_amount,
        }
        results = self.query(query_str, variables)

        return results

    def get_orders(
        self,
        status: str,
        side: str = None,
        cryptocurrency: str = "bitcoin",
        query_str: str = GET_ORDERS,
    ) -> Dict[str, Dict[str, Any]]:

        """
        Retrieve a list of orders.

        Parameters
        ----------
        status: str
            The state of the transaction - "open" | "completed".
        side : str, optional
            The type of transaction - "buy" | "sell".
        cryptocurrency: str, optional
            The cryptocurrency type involved in the transaction
            (default is bitcoin).
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_ORDERS).

        Returns
        -------
        results : dict
            A dictionary containing a list of orders placed by the
            authenticated user.
        """

        _ = validator(side=side, status=status, currency=cryptocurrency)

        variables = {
            "cryptocurrency": cryptocurrency,
            "side": side,
            "status": status,
        }
        results = self.query(query_str, variables)

        return results

    def get_payments(
        self, query_str: str = GET_PAYMENTS
    ) -> Dict[str, Dict[str, Any]]:

        """
        Retrieves a list of payments.

        Parameters
        ----------
        query_str : str, optional
            This is the GraphQL query in string format (Default
            is GET_PAYMENTS)
        """

        variables = {}
        results = self.query(query_str)

        return results

    def get_prices(
        self,
        side: str = None,
        cryptocurrency: str = None,
        query_str: str = GET_PRICES,
    ) -> Dict[str, List[Dict[str, Any]]]:

        """
        Retrieve buy/sell price(s) for supported cryptocurrencies.

        Parameters
        ----------
        side : str
            The type of transaction - "buy" | "sell".
        cryptocurrency: str
            The cryptocurrency type involved in the transaction.
        query_str : str, optional
            This is the GraphQL query in string format (default
            is GET_ORDERS).

        Returns
        -------
        results : dict
            A dictionary containing active price .
        """

        if side or cryptocurrency:
            _ = validator(side=side, currency=cryptocurrency)

        variables = {"cryptocurrency": cryptocurrency, "side": side}
        results = self.query(query_str, variables)

        return results
