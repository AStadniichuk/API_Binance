import logging

from tortoise import Tortoise

from models.exchange_rate import ExchangeRate
from api_clients.abstract_client import AbstractAPIClient

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite://../db.sqlite3"


class SQLClient(AbstractAPIClient):
    """
        Client to save data to SQLite database and output information to log.

        Args:
            currency_pair (str): A currency pair (e.g., 'BTCUSDT').
            interval (int): The time interval between API requests (in seconds).
    """

    def __init__(self, currency_pair: str, interval: int):
        super().__init__(currency_pair, interval)

    async def _save_to_database(self, price: float) -> None:
        await ExchangeRate.create(currency_pair=self.currency_pair, price=price)

    async def display_info(self, price: float) -> None:
        await self._save_to_database(price)
        current_time = await self.get_current_time()
        logging.info(f"{self.currency_pair} - Time: {current_time}, Price: {price}")
        await Tortoise.close_connections()
