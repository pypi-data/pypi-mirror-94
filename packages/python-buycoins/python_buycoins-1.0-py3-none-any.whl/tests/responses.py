# Query responses

get_balance = {
    "data": {
        "getBalances": [
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "bitcoin",
                "confirmedBalance": "0.0",
            }
        ]
    }
}

get_balances = {
    "data": {
        "getBalances": [
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "bitcoin",
                "confirmedBalance": "0.0",
            },
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "usd_tether",
                "confirmedBalance": "0.0",
            },
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "naira_token",
                "confirmedBalance": "0.0",
            },
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "ethereum",
                "confirmedBalance": "0.0",
            },
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "litecoin",
                "confirmedBalance": "0.0",
            },
            {
                "id": "QWNjb3VudC0=",
                "cryptocurrency": "usd_coin",
                "confirmedBalance": "0.0",
            },
        ]
    }
}

get_bank_accounts = {
    "data": {
        "getBankAccounts": [
            {
                "id": "QmFua0FjY291bnQtNjlkZGM2MjEtYzM0My00Mzg1LTlkMDYtY2VkNTM2MWY1Yjkz",
                "bankName": "ALAT by WEMA",
                "accountName": "kolapo ayesebotan",
                "accountNumber": "0235959654",
                "accountType": "withdrawal",
                "accountReference": None,
            }
        ]
    }
}

get_estimated_network_fee_default = {
    "data": {
        "getEstimatedNetworkFee": {
            "total": "0.03036",
            "estimatedFee": "0.00036",
        }
    }
}

get_estimated_network_fee_ethereum = {
    "data": {
        "getEstimatedNetworkFee": {"total": "0.04", "estimatedFee": "0.01"}
    }
}

# The data below was truncated
get_market_book_default = {
    "data": {
        "getMarketBook": {
            "dynamicPriceExpiry": 1612808872,
            "orders": {
                "edges": [
                    {
                        "node": {
                            "id": "UG9zdE9yZGVyLTcxY2JmZjAxLTk2NTEtNGQzOC1hMGIyLWE2YzRkMDUzNWVkMA==",
                            "cryptocurrency": "bitcoin",
                            "coinAmount": "0.013797",
                            "side": "buy",
                            "status": "active",
                            "createdAt": 1612808624,
                            "pricePerCoin": "19501000.0",
                            "priceType": "static",
                            "staticPrice": "1950100000",
                            "dynamicExchangeRate": None,
                        }
                    },
                    {
                        "node": {
                            "id": "UG9zdE9yZGVyLTM5ODg2ZTNlLTJmZDQtNDgxNy05ODRjLWNlMTFlYmIwMzhlMw==",
                            "cryptocurrency": "bitcoin",
                            "coinAmount": "0.00653659",
                            "side": "sell",
                            "status": "active",
                            "createdAt": 1612800454,
                            "pricePerCoin": "20500000.0",
                            "priceType": "static",
                            "staticPrice": "2050000000",
                            "dynamicExchangeRate": None,
                        }
                    },
                ]
            },
        }
    }
}

# The data below was truncated
get_market_book_usd_tether = {
    "data": {
        "getMarketBook": {
            "dynamicPriceExpiry": 1612810492,
            "orders": {
                "edges": [
                    {
                        "node": {
                            "id": "UG9zdE9yZGVyLWZmYTliOTdiLThmZjUtNDE4Mi05ZDJjLWM4ZWM5MzNlMTliZg==",
                            "cryptocurrency": "usd_tether",
                            "coinAmount": "100.0",
                            "side": "buy",
                            "status": "active",
                            "createdAt": 1611770385,
                            "pricePerCoin": "460.0",
                            "priceType": "static",
                            "staticPrice": "46000",
                            "dynamicExchangeRate": None,
                        }
                    },
                    {
                        "node": {
                            "id": "UG9zdE9yZGVyLWI5ZWJkYWNmLTQ1MjYtNDYxYS1hYzFlLTljZTZlNTRmOWFkOA==",
                            "cryptocurrency": "usd_tether",
                            "coinAmount": "234.0",
                            "side": "sell",
                            "status": "active",
                            "createdAt": 1612413166,
                            "pricePerCoin": "499.0",
                            "priceType": "static",
                            "staticPrice": "49900",
                            "dynamicExchangeRate": None,
                        }
                    },
                ]
            },
        }
    }
}

get_orders = {
    "data": {
        "getOrders": {
            "dynamicPriceExpiry": 1612811512,
            "orders": {
                "edges": [
                    {
                        "node": {
                            "id": "UG9zdE9yZGVyLWEzYTAwNzQxLTJhMWUtNGJkMi1iZWFkLWE2ZWU0MzQ1ZmI2Yw==",
                            "cryptocurrency": "bitcoin",
                            "coinAmount": "0.005",
                            "side": "buy",
                            "status": "active",
                            "createdAt": 1605000847,
                            "pricePerCoin": "10900.09",
                            "priceType": "static",
                            "staticPrice": "1090009",
                            "dynamicExchangeRate": None,
                        }
                    }
                ]
            },
        }
    }
}

get_payments = {
    "data": {
        "getPayments": {
            "edges": [
                {
                    "node": {
                        "id": "UG9zdE9yZGVyLTg5MDM4MzI4LTc5MzItNGUxMS1hZWZjLTkwYjg4ZTFhY2JjOA==",
                        "fee": "0.0046",
                        "amount": "10000.00",
                        "createdAt": 1605000847,
                        "reference": "38d5d9018bde98e88058746788d72e936d158f5ad753073f4763dc1d4aa5a48e",
                        "status": "success",
                        "totalAmount": "10000.004600",
                        "type": "deposit",
                    }
                }
            ]
        }
    }
}

get_price = {
    "data": {
        "getPrices": [
            {
                "id": "QnV5Y29pbnNQcmljZS0yOWFmZWY4MS1mZjI5LTQwYTQtYmQ3Zi1iOTgzMTA3NmU5NDg=",
                "status": "active",
                "cryptocurrency": "ethereum",
                "minBuy": "0.02",
                "minSell": "0.02",
                "maxBuy": "48.07685652",
                "maxSell": "0",
                "minCoinAmount": "0.02",
                "expiresAt": 1612847332,
                "buyPricePerCoin": "816107.8759",
                "sellPricePerCoin": "799786.8945",
            }
        ]
    }
}

get_prices = {
    "data": {
        "getPrices": [
            {
                "id": "QnV5Y29pbnNQcmljZS01OTkwYTQ0NC1hYjY4LTQxM2MtODUzZC04OWJhYzRhMWNjZjE=",
                "status": "active",
                "cryptocurrency": "bitcoin",
                "minBuy": "0.001",
                "minSell": "0.001",
                "maxBuy": "1.78700697",
                "maxSell": "1.20119207",
                "minCoinAmount": "0.001",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "21956210.523",
                "sellPricePerCoin": "21521388.24",
            },
            {
                "id": "QnV5Y29pbnNQcmljZS05MjQwNmQ0Zi00MmJlLTQ2MjEtOTY1Ny1mYTM0OGZkNmI2NDE=",
                "status": "active",
                "cryptocurrency": "ethereum",
                "minBuy": "0.02",
                "minSell": "0.02",
                "maxBuy": "48.12180182",
                "maxSell": "0",
                "minCoinAmount": "0.02",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "815345.6391",
                "sellPricePerCoin": "799154.344",
            },
            {
                "id": "QnV5Y29pbnNQcmljZS04NDMyZmI2OS1iMzAyLTQ2YzQtYjFjZC1kZTM2MjNhMTFiYmU=",
                "status": "active",
                "cryptocurrency": "litecoin",
                "minBuy": "0.1",
                "minSell": "0.1",
                "maxBuy": "489.37725284",
                "maxSell": "134.73978949",
                "minCoinAmount": "0.1",
                "expiresAt": 1612847213,
                "buyPricePerCoin": "80175.1635",
                "sellPricePerCoin": "78560.0343",
            },
            {
                "id": "QnV5Y29pbnNQcmljZS05OGI0NTE5ZC05NTJlLTRkNGMtODk1OC03MWI2MjRlZmZlMjc=",
                "status": "active",
                "cryptocurrency": "usd_coin",
                "minBuy": "5",
                "minSell": "5",
                "maxBuy": "83903.73",
                "maxSell": "495437.574734",
                "minCoinAmount": "5",
                "expiresAt": 1612847213,
                "buyPricePerCoin": "467.63",
                "sellPricePerCoin": "458.3206",
            },
        ]
    }
}


# Mutation responses

buy_default = {
    "data": {
        "buy": {
            "id": "QnV5Y29pbnNQcmljZS11MENzAnJ31T2jNaBzMRR3ZaRuZkGkAD2lAUN3NkMiNUGjAnV=",
            "price": {
                "id": "QnV5Y29pbnNQcmljZS01OTkwYTQ0NC1hYjY4LTQxM2MtODUzZC04OWJhYzRhMWNjZjE=",
                "status": "active",
                "cryptocurrency": "bitcoin",
                "minBuy": "0.001",
                "minSell": "0.001",
                "maxBuy": "1.78700697",
                "maxSell": "1.20119207",
                "minCoinAmount": "0.001",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "21956210.523",
                "sellPricePerCoin": "21521388.24",
            },
            "cryptocurrency": "bitcoin",
            "filledCoinAmount": "1.230000",
            "side": "buy",
            "status": "pending",
            "totalCoinAmount": "0.03",
            "createdAt": 1612847212,
        }
    }
}

buy_ethereum = {
    "data": {
        "buy": {
            "id": "QnV5Y29pbnNQcmljZS16iR364whgHoYiAMsKGpxJEWIZmOTjqz7OssziZyAbtnlSVC=",
            "price": {
                "id": "QnV5Y29pbnNQcmljZS05MjQwNmQ0Zi00MmJlLTQ2MjEtOTY1Ny1mYTM0OGZkNmI2NDE=",
                "status": "active",
                "cryptocurrency": "ethereum",
                "minBuy": "0.02",
                "minSell": "0.02",
                "maxBuy": "48.12180182",
                "maxSell": "0",
                "minCoinAmount": "0.02",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "815345.6391",
                "sellPricePerCoin": "799154.344",
            },
            "cryptocurrency": "ethereum",
            "filledCoinAmount": "3.223432",
            "side": "buy",
            "status": "done",
            "totalCoinAmount": "1.3",
            "createdAt": 1612847212,
        }
    }
}

cancel_withdrawal = {
    "data": {
        "cancelWithdrawal": {
            "id": "QWRkcmVzcy1hz8V54ffgpB2pX52m8IG2fMgToM2ln5H3k3QJYNyShpz8EiF=",
            "fee": "0.046",
            "amount": "100000.00",
            "createdAt": 1612847212,
            "reference": "zmJxqDM3-dz_sPoi7LwalRM5N8Q711BllncBuq476xw",
            "status": "pending",
            "totalAmount": "100000.046",
            "type": "withdrawal",
        }
    }
}

create_address_default = {
    "data": {
        "createAddress": {
            "id": "QWRkcmVzcy1hMWU2YTRlMy1iOTBhLTQwMWEtOWNkZS00OTM5NWZlOWIzZWY=",
            "address": "39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8",
            "cryptocurrency": "bitcoin",
            "createdAt": 1612857009,
        }
    }
}

create_address_ethereum = {
    "data": {
        "createAddress": {
            "id": "QWRkcmVzcy05NmQyZDdmNS05NDgxLTQwODMtODdlOC01ZjdmM2QwODZiYzg=",
            "address": "0x64b82318cadaf1209b16726d5634455762748a90",
            "cryptocurrency": "ethereum",
            "createdAt": 1612857154,
        }
    }
}

create_deposit_account = {
    "data": {
        "createDepositAccount": {
            "id": "QmFua0FjY291bnTffyORgTFvah6zcxBllmkbEcJb6gQigoWKwbl6yCP2MWY1Yjkz",
            "bankName": "Providus Bank",
            "accountName": "Dummy User",
            "accountNumber": "9008007000",
            "accountType": "deposit",
            "accountReference": "3T3B_3TM9kuf-rBenmSvN-RL",
        }
    }
}

create_withdrawal = {
    "data": {
        "createWithdrawal": {
            "id": "QWRkcmVzcy1hz8V5vMlQ1f4Kk9MUziKwKdtiOAll2qPRpdve6S4wWaUBeYk=",
            "fee": "0.046",
            "amount": "100000.00",
            "createdAt": 1612867302,
            "reference": "hPm000GJBexlW2cfeYsalonCwTxzSXNwh-QoAEv_A8s",
            "status": "pending",
            "totalAmount": "100000.046",
            "type": "withdrawal",
        }
    }
}

post_limit_order = {
    "data": {
        "postLimitOrder": {
            "id": "UG9zdE9yZGVyLWYyNGMzNmVlLTAwZmMtNGM1Ny04MmJkLWYzOGI4ZTA0MTAxMw==",
            "cryptocurrency": "bitcoin",
            "coinAmount": "0.00819931",
            "side": "buy",
            "status": "inactive",
            "createdAt": 1612867863,
            "pricePerCoin": "2205000000.0",
            "priceType": "static",
            "staticPrice": "220500000000",
            "dynamicExchangeRate": None,
        }
    }
}

post_market_order = {
    "data": {
        "postMarketOrder": {
            "id": "UG9zdE9yZGVyLWYyNGMzHMGTaSx0XuVMIiI7qXyRnZ7MzuooxOApisAuIov3k8==",
            "cryptocurrency": "bitcoin",
            "coinAmount": "0.0004",
            "side": "sell",
            "status": "active",
            "createdAt": 1612867873,
            "pricePerCoin": "2205000000.0",
            "priceType": "static",
            "staticPrice": "220500000000",
            "dynamicExchangeRate": None,
        }
    }
}

sell_default = {
    "data": {
        "sell": {
            "id": "QnV5Y29pbnNQcmljZS11KSkCEauCpTyq3vbbW6TKrjIfwfvjcVJYvomfKOtJTRwjAnV=",
            "price": {
                "id": "QnV5Y29pbnNQcmljZS01OTkwYTQ0NC1hYjY4LTQxM2MtODUzZC04OWJhYzRhMWNjZjE=",
                "status": "active",
                "cryptocurrency": "bitcoin",
                "minBuy": "0.001",
                "minSell": "0.001",
                "maxBuy": "1.78700697",
                "maxSell": "1.20119207",
                "minCoinAmount": "0.001",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "21956210.523",
                "sellPricePerCoin": "21521388.24",
            },
            "cryptocurrency": "bitcoin",
            "filledCoinAmount": "1.230000",
            "side": "sell",
            "status": "pending",
            "totalCoinAmount": "0.03",
            "createdAt": 1612847212,
        }
    }
}

sell_ethereum = {
    "data": {
        "sell": {
            "id": "QnV5Y29pbnNQcmljZS16CZ3R79tuZUJFTSCaWzqnMKe0a17EWh35i1WZhdW5Mg8SVC=",
            "price": {
                "id": "QnV5Y29pbnNQcmljZS05MjQwNmQ0Zi00MmJlLTQ2MjEtOTY1Ny1mYTM0OGZkNmI2NDE=",
                "status": "active",
                "cryptocurrency": "ethereum",
                "minBuy": "0.02",
                "minSell": "0.02",
                "maxBuy": "48.12180182",
                "maxSell": "0",
                "minCoinAmount": "0.02",
                "expiresAt": 1612847212,
                "buyPricePerCoin": "815345.6391",
                "sellPricePerCoin": "799154.344",
            },
            "cryptocurrency": "ethereum",
            "filledCoinAmount": "3.223432",
            "side": "sell",
            "status": "done",
            "totalCoinAmount": "1.3",
            "createdAt": 1612847212,
        }
    }
}

send = {
    "data": {
        "send": {
            "id": "QnV5Y29pbnNQcmljZS16CZ3RctvVxtbTeS51jh1aQrmCZkxoMdKw8isRG89UbZovH4=",
            "fee": "0.00024",
            "amount": "0.2",
            "address": "39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8",
            "cryptocurrency": "bitcoin",
            "status": "processing",
            "transaction": {
                "id": "QnV5Y29pbnNQcmljZS16CZ3RctvVxtAP99KXU9M9nYA2Atqs3CU1nBvdZWnWmt1soY=",
                "address": {
                    "id": "QWRkcmVzcy05NmQyZDdmNS05NDgxLTQwODMtODdlOC01ZjdmM2QwODZiYzg=",
                    "cryptocurrency": "bitcoin",
                    "address": "39pxTA36PmUokoKEnHB41Lg8Kh2uw6q8o8",
                    "createdAt": 1612857154,
                },
                "txhash": "8223715e93f1c8715a8070b323acee111c1cadeb1eff16fe44b60e4269c175ab",
                "amount": "0.2",
                "confirmed": False,
                "cryptocurrency": "bitcoin",
                "direction": "outgoing",
                "createdAt": 1612871202,
            },
            "createdAt": 1612871202,
        }
    }
}

send_off_chain = {
    "data": {
        "sendOffchain": {
            "initiated": True
        }
    }
}
