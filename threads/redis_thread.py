import asyncio

from api_clients.redis_client import RedisClient
from threads.abstract_thread import AbstractThread


class RedisClientThread(AbstractThread):
    def __init__(self, currency_pair, interval):
        super().__init__(currency_pair, interval)
        self.client_instance = RedisClient(currency_pair, interval)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.client_instance.start_polling())
