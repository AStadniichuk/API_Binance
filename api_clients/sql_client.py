import asyncio
import logging
from datetime import datetime

from models.exchange_rate import ExchangeRate
from api_clients.abstract_client import AbstractAPIClient
from tortoise_config import db_manager
from utils.price_chart_builder import GraphBuilder

DATABASE_URL = "sqlite://../db.sqlite3"


class SQLClient(AbstractAPIClient):
    """
    Client to save data to SQLite database and output information to log.

    Args:
        currency_pair (str): A currency pair (e.g., 'BTCUSDT').
        interval (int): The time interval between API requests (in seconds).
        max_iterations (int | None): The maximum number of iterations to perform (optional).
    """

    def __init__(self, currency_pair: str, interval: int, max_iterations: int | None = None):
        super().__init__(currency_pair, interval, max_iterations)

    async def _save_to_database(self, price: float) -> None:
        try:
            await ExchangeRate.create(currency_pair=self.currency_pair, price=price)

        except Exception as error:
            logging.error(f'Error saving to database: {str(error)}')

    async def _log_price_info(self, price: float) -> None:
        try:
            current_time = await self.get_current_time()
            logging.info(f"{self.currency_pair} - Time: {current_time}, Price: {price}")

        except Exception as error:
            logging.error(f'Error log price info {str(error)}')

    async def get_exchange_rates(self) -> list[ExchangeRate]:
        try:
            exchange_rates = await ExchangeRate.all()
            return exchange_rates

        except Exception as error:
            logging.error(f'Error retrieving exchange rates from the database: {str(error)}')

    @staticmethod
    async def create_exchange_rate_dict(exchange_rates: list[ExchangeRate]) -> dict[datetime, float]:
        return {rate.timestamp: rate.price for rate in exchange_rates}

    async def start_sql_client(self) -> None:
        await db_manager.initialize_db()
        await self.start_polling()
        exchange_rates = await self.create_exchange_rate_dict(await self.get_exchange_rates())
        await db_manager.close_connection()

        graph = GraphBuilder(self.currency_pair, exchange_rates)
        graph.show_graph()

    def run(self) -> None:
        asyncio.run(self.start_sql_client())
