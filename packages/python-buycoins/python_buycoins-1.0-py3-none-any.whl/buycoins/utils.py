allowed_sides = ["buy", "sell"]

allowed_statuses = ["open", "completed"]

allowed_currencies = [
    "usd_coin",
    "bitcoin",
    "ethereum",
    "litecoin",
    "usd_tether",
    "naira_token",
]

allowed_price_types = ["static", "dynamic"]


def validator(
    side: str = None,
    status: str = None,
    currency: str = None,
    price_type: str = None,
) -> None:
    if side and side not in allowed_sides:
        raise ValueError("Invalid side!")

    if status and status not in allowed_statuses:
        raise ValueError("Invalid status!")

    if currency and currency not in allowed_currencies:
        raise ValueError("Invalid or unsupported currency!")

    if price_type and price_type not in allowed_price_types:
        raise ValueError("Invalid price type!")
