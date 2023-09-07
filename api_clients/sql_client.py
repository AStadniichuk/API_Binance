import logging

from tortoise import Tortoise

from models.exchange_rate import ExchangeRate
from api_clients.abstract_client import AbstractAPIClient

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite://../db.sqlite3"


class SQLClient(AbstractAPIClient):
    def __init__(self, currency_pair, interval):
        super().__init__(currency_pair, interval)

    async def _save_to_database(self, price):
        await ExchangeRate.create(currency_pair=self.currency_pair, price=price)

    async def display_info(self, price):
        await self._save_to_database(price)
        current_time = await self.get_current_time()
        logging.info(f"{self.currency_pair} - Time: {current_time}, Price: {price}")
        await Tortoise.close_connections()
