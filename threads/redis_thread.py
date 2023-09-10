import asyncio

from api_clients.redis_client import RedisClient
from threads.abstract_thread import AbstractThread


class RedisClientThread(AbstractThread):
    """
    A threading client to work with Redis.

        Attributes:
            client_instance (SQLClient): An instance of the client for working with the SQL database.

        Args:
            currency_pair (str): The currency pair the client is working with.
            interval (int): The time interval between requests to the API.
    """

    def __init__(self, currency_pair: str, interval: int):
        super().__init__(currency_pair, interval)
        self.client_instance = RedisClient(currency_pair, interval)

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.client_instance.start_polling())
