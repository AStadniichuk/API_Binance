from string import ascii_uppercase

def verify_currency_pair(currency_pair: str):
    """Verify the format of a currency pair."""
    if not isinstance(currency_pair, str):
        raise TypeError("Currency pair must be a string")

    currency_pair = currency_pair.upper()

    if not currency_pair:
        raise ValueError('Currency pair cannot be unspecified')

    for char in currency_pair:
        if not char in ascii_uppercase:
            raise ValueError('Currency pair can only contain letters of the English alphabet')


def verify_interval(interval: int):
    """Verify the format of an interval."""

    if not isinstance(interval, int):
        raise TypeError("Interval must be a int")

    if interval < 1:
        raise ValueError("Interval must be greater than or equal to 1")
