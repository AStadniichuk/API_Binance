import json
import logging
import random
from datetime import datetime

import redis
import asyncio

from api_clients.abstract_client import AbstractAPIClient
from utils.price_chart_builder import GraphBuilder


class RedisClient(AbstractAPIClient):
    """
        Client to save data to Redis and output information.

        Args:
            currency_pair (str): A currency pair (e.g., 'BTCUSDT').
            interval (int): The time interval between API requests (in seconds).
            max_iterations (int | None): The maximum number of iterations to perform (optional).
        """

    def __init__(self, currency_pair: str, interval: int, max_iterations: int | None = None):
        super().__init__(currency_pair, interval, max_iterations)
        self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)

    async def _save_to_database(self, price: float) -> None:
        try:
            current_time = await self.get_current_time()
            currency_data = {self.currency_pair: price}
            currency_json = json.dumps(currency_data)

            await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.set, current_time, currency_json)
            await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.expire, current_time, 86400)

        except Exception as error:
            logging.error(f'Error saving to Redis: {str(error)}')

    async def _log_price_info(self, price: float) -> None:
        try:
            current_time = await self.get_current_time()
            logging.info(f"{self.currency_pair} - Time: {current_time}, Price: {price}")
            random_number = random.randint(1, 10)
            logging.info(f"Random Number: {random_number}")

        except Exception as error:
            logging.error(f'Error log price info {str(error)}')

    async def get_exchange_rates(self) -> dict[datetime, float]:
        try:
            exchange_rates = {}
            times = await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.keys, '*')

            for time in times:
                time_str = time.decode('utf-8')
                rate_str = await asyncio.get_event_loop().run_in_executor(None, self.redis_connection.get, time_str)
                if rate_str:
                    rate = json.loads(rate_str.decode('utf-8'))
                    currency_value = rate.get(self.currency_pair)
                    if currency_value is not None:
                        time = datetime.strptime(time_str, '%Y.%m.%d %H:%M:%S')
                        exchange_rates[time] = float(currency_value)
                        exchange_rates = {rate[0]: rate[1] for rate in sorted(exchange_rates.items())}
            return exchange_rates

        except Exception as error:
            logging.error(f'Error retrieving data from Redis: {str(error)}')

    async def start_redis_client(self) -> None:
        await self.start_polling()

        graph = GraphBuilder(self.currency_pair, await self.get_exchange_rates())
        graph.show_graph()

    def run(self) -> None:
        asyncio.run(self.start_redis_client())
