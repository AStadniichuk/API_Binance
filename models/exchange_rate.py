from tortoise import fields, Model


class ExchangeRate(Model):
    id = fields.IntField(pk=True)
    currency_pair = fields.CharField(max_length=20)
    price = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)
