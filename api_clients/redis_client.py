import json
import logging
import random

import redis
import asyncio

from api_clients.abstract_client import AbstractAPIClient


class RedisClient(AbstractAPIClient):
    """
        Client to save data to Redis and output information.

        Args:
            currency_pair (str): A currency pair (e.g., 'BTCUSDT').
            interval (int): The time interval between API requests (in seconds).
    """

    def __init__(self, currency_pair: str, interval: int):
        super().__init__(currency_pair, interval)
        self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)

    async def _save_to_database(self, price: float) -> None:
        current_time = await self.get_current_time()
        currency_data = {self.currency_pair: price}
        currency_json = json.dumps(currency_data)

        await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.set, current_time, currency_json)
        await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.expire, current_time, 86400)

    async def display_info(self, price: float) -> None:
        await self._save_to_database(price)
        current_time = await self.get_current_time()
        logging.info(f"{self.currency_pair} - Time: {current_time}, Price: {price}")
        random_number = random.randint(1, 10)
        logging.info(f"Random Number: {random_number}")
