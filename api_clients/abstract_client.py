import logging
import os
import httpx
import asyncio

from threading import Thread
from datetime import datetime

from yarl import URL
from abc import ABC, abstractmethod

from validators.validators import verify_all
from config import BINANCE_URL

logging.basicConfig(level=logging.INFO)


class AbstractAPIClient(Thread, ABC):
    """
       An abstract base class for API clients that run in a separate thread.

       Args:
           currency_pair (str): A currency pair (e.g., 'BTCUSDT').
           interval (int): The time interval between API requests (in seconds).
           max_iterations (int | None): The maximum number of iterations to perform (optional).
    """
    currency_pair: str
    interval: int
    api_endpoint: str
    max_iterations: int | None

    def __init__(self, currency_pair: str, interval: int, max_iterations: int | None = None):
        verify_all(currency_pair, interval)

        super().__init__()
        self.currency_pair = currency_pair.upper()
        self.interval = interval
        self.api_endpoint = os.getenv('BINANCE_URL', BINANCE_URL)
        self.max_iterations = max_iterations
        self._iteration_counter: int = 0

    @abstractmethod
    async def _save_to_database(self, price: float) -> None:
        pass

    @abstractmethod
    async def _log_price_info(self, prise: float) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    async def fetch_exchange_rate(self) -> float:
        async with httpx.AsyncClient() as client:
            url = str(URL(self.api_endpoint))
            params = {'symbol': self.currency_pair}

            response = await client.get(url=url, params=params)
            data = response.json()
            return data["price"]

    async def display_info(self, price: float) -> None:
        await self._save_to_database(price)
        await self._log_price_info(price)

    async def start_polling(self) -> None:
        while not self.should_stop_polling():
            try:
                exchange_rate = await self.fetch_exchange_rate()
                await self.display_info(exchange_rate)
                await asyncio.sleep(self.interval)

                if self.max_iterations is not None:
                    self._iteration_counter += 1
            except Exception as error:
                logging.error(str(error))

    def should_stop_polling(self):
        if self.max_iterations is not None:
            return self._iteration_counter >= self.max_iterations

    @staticmethod
    async def get_current_time() -> str:
        return datetime.now().strftime("%Y.%m.%d %H:%M:%S")
