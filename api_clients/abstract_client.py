import os
import httpx
import asyncio

from datetime import datetime

from yarl import URL
from abc import ABC, abstractmethod

from validators.validators import verify_interval, verify_currency_pair
from config import BINANCE_URL


class AbstractAPIClient(ABC):
    currency_pair: str
    interval: int
    api_endpoint: str

    def __init__(self, currency_pair: str, interval: int):
        verify_currency_pair(currency_pair)
        verify_interval(interval)

        self.currency_pair = currency_pair.upper()
        self.interval = interval
        self.api_endpoint = os.getenv('BINANCE_URL', BINANCE_URL)

    @abstractmethod
    async def _save_to_database(self, price):
        pass

    @abstractmethod
    async def display_info(self, price):
        pass

    async def fetch_exchange_rate(self):
        async with httpx.AsyncClient() as client:
            url = str(URL(self.api_endpoint))
            params = {'symbol': self.currency_pair}

            response = await client.get(url=url, params=params)
            data = response.json()
            return data["price"]

    async def start_polling(self):
        while True:
            exchange_rate = await self.fetch_exchange_rate()
            await self.display_info(exchange_rate)
            await asyncio.sleep(self.interval)

    @staticmethod
    async def get_current_time():
        return datetime.now().strftime("%Y.%m.%d %H:%M:%S")