"""
This contains all query strings
"""


# Queries

GET_BALANCES = """
    query getBalances($cryptocurrency: Cryptocurrency) {
        getBalances(cryptocurrency: $cryptocurrency) {
            id
            cryptocurrency
            confirmedBalance
        }
    }
"""

GET_BANK_ACCOUNTS = """
    query getBankAccounts($accountNumber: String) {
        getBankAccounts(accountNumber: $accountNumber) {
            id
            bankName
            accountName
            accountNumber
            accountType
            accountReference
        }
    }
"""

GET_ESTIMATED_NETWORK_FEE = """
    query getEstimatedNetworkFee(
        $cryptocurrency: Cryptocurrency, $amount: BigDecimal!
    ) {
        getEstimatedNetworkFee(cryptocurrency: $cryptocurrency, amount: $amount) {
            total
            estimatedFee
        }
    }
"""

GET_MARKET_BOOK = """
    query getMarketBook(
        $cryptocurrency: Cryptocurrency, $coinAmount: BigDecimal
    ) {
        getMarketBook(cryptocurrency: $cryptocurrency, coinAmount: $coinAmount) {
            dynamicPriceExpiry
            orders {
                edges {
                    node {
                        id
                        cryptocurrency
                        coinAmount
                        side
                        status 
                        createdAt
                        pricePerCoin
                        priceType
                        staticPrice
                        dynamicExchangeRate
                    }
                }
            }
        }
    }
"""

GET_ORDERS = """
    query getOrders(
        $cryptocurrency: Cryptocurrency, $status: GetOrdersStatus!, $side: OrderSide
    ) {
        getOrders(cryptocurrency: $cryptocurrency, status: $status, side: $side) {
            dynamicPriceExpiry
            orders {
                edges {
                    node {
                        id
                        cryptocurrency
                        coinAmount
                        side
                        status
                        createdAt
                        pricePerCoin
                        priceType
                        staticPrice
                        dynamicExchangeRate
                    }
                }
            }
        }
    }
"""

GET_PAYMENTS = """
    query getPayments {
        getPayments {
            edges {
                node {
                    id
                    fee
                    amount
                    createdAt
                    reference
                    status
                    totalAmount
                    type
                }
            }
        }
    }
"""

GET_PRICES = """
    query getPrices($cryptocurrency: Cryptocurrency, $side: OrderSide) {
        getPrices(cryptocurrency: $cryptocurrency, side: $side) {
            id
            status
            cryptocurrency
            minBuy
            minSell
            maxBuy
            maxSell
            minCoinAmount
            expiresAt
            buyPricePerCoin
            sellPricePerCoin
        }
    }
"""


# Mutations

BUY = """
    mutation buy(
        $cryptocurrency: Cryptocurrency, $price: ID!, $coin_amount: BigDecimal!
    ) {
        buy(
            cryptocurrency: $cryptocurrency, price: $price, coin_amount: $coin_amount
        ) {
            id
            price {
                id
                status
                cryptocurrency
                minBuy
                minSell
                maxBuy
                maxSell
                minCoinAmount
                expiresAt
                buyPricePerCoin
                sellPricePerCoin
            }
            cryptocurrency
            filledCoinAmount
            side
            status
            totalCoinAmount
            createdAt
        }
    }
"""

CANCEL_WITHDRAWAL = """
    mutation cancelWithdrawal($payment: ID!) {
        cancelWithdrawal(payment: $payment) {
            id
            fee
            amount
            createdAt
            reference
            status
            totalAmount
            type            
        }
    }
"""

CREATE_ADDRESS = """
    mutation createAddress($cryptocurrency: Cryptocurrency) {
        createAddress(cryptocurrency: $cryptocurrency) {
            id
            address
            cryptocurrency
            createdAt
        }
    }
"""

CREATE_DEPOSIT_ACCOUNT = """
    mutation createDepositAccount($accountName: String!) {
        createDepositAccount(accountName: $accountName) {
            id
            bankName
            accountName
            accountNumber
            accountType
            accountReference
        }
    }
"""

CREATE_WITHDRAWAL = """
    mutation createWithdrawal($bankAccount: ID!, $amount: BigDecimal!) {
        createWithdrawal(bankAccount: $bankAccount, amount: $amount) {
            id
            fee
            amount
            createdAt
            reference
            status
            totalAmount
            type
        }
    }
"""

POST_LIMIT_ORDER = """
    mutation postLimitOrder(
        $cryptocurrency: Cryptocurrency, $orderSide: OrderSide!, $coinAmount: BigDecimal!,
        $staticPrice: BigDecimal, $priceType: PriceType!, $dynamicExchangeRate: BigDecimal
    ) {
        postLimitOrder(
            cryptocurrency: $cryptocurrency, orderSide: $orderSide, coinAmount: $coinAmount,
            staticPrice: $staticPrice, priceType: $priceType, dynamicExchangeRate: $dynamicExchangeRate
        ) {
            id
            cryptocurrency
            coinAmount
            side
            status
            createdAt
            pricePerCoin
            priceType
            staticPrice
            dynamicExchangeRate
        }
    }
"""

POST_MARKET_ORDER = """
    mutation postMarketOrder(
        $cryptocurrency: Cryptocurrency, $orderSide: OrderSide!, $coinAmount: BigDecimal!
    ) {
        postMarketOrder(
            cryptocurrency: $cryptocurrency, orderSide: $orderSide, coinAmount: $coinAmount
        ) {
            id
            cryptocurrency
            coinAmount
            side
            status
            createdAt
            pricePerCoin
            priceType
            staticPrice
            dynamicExchangeRate
        }
    }
"""

SELL = """
    mutation sell(
        $cryptocurrency: Cryptocurrency, $price: ID!, $coin_amount: BigDecimal!
    ) {
        sell(
            cryptocurrency: $cryptocurrency, price: $price, coin_amount: $coin_amount
        ) {
            id
            price {
                id
                status
                cryptocurrency
                minBuy
                minSell
                maxBuy
                maxSell
                minCoinAmount
                expiresAt
                buyPricePerCoin
                sellPricePerCoin
            }
            cryptocurrency
            filledCoinAmount
            side
            status
            totalCoinAmount
            createdAt
        }
    }
"""

SEND = """
    mutation send(
        $cryptocurrency: Cryptocurrency, $address: String!, $amount: BigDecimal!
    ) {
        send(
            cryptocurrency: $cryptocurrency, address: $address, amount: $amount
        ) {
            id
            fee
            amount
            address
            cryptocurrency
            status
            transaction {
                id
                address {
                    id
                    cryptocurrency
                    address
                    createdAt
                }
                txhash
                amount
                confirmed
                cryptocurrency
                direction
                createdAt
            }
            createdAt
        }
    }
"""

SEND_OFF_CHAIN = """
    mutation sendOffchain(
        $cryptocurrency: Cryptocurrency, $amount: BigDecimal!, $recipient: String!
    ) {
        sendOffchain(
            cryptocurrency: $cryptocurrency, amount: $amount, recipient: $recipient
        ) {
            initiated
        }
    }
"""
