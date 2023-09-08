from tortoise import fields, Model


class ExchangeRate(Model):
    """
        A model to store the exchange rate between currencies.

        Attributes:
            id (int): The unique identifier of the record.
            currency_pair (str): The currency pair for which the exchange rate is stored (e.g. 'BTCUSDT').
            price (float): The value of the exchange rate.
            timestamp (datetime.datetime): The date and time when the record was saved (automatically appended).
    """
    id = fields.IntField(pk=True)
    currency_pair = fields.CharField(max_length=20)
    price = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)
