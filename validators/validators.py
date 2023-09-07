def verify_currency_pair(currency_pair: str):
    if not isinstance(currency_pair, str):
        raise TypeError("Currency pair must be a string")

    if not currency_pair:
        raise ValueError('Currency pair cannot be unspecified')

    for char in currency_pair:
        if not char.isalpha():
            raise ValueError('Currency pair can only contain letters')


def verify_interval(interval: int):
    if not isinstance(interval, int):
        raise TypeError("Interval must be a int")

    if interval < 1:
        raise ValueError("Interval must be greater than or equal to 1")