import asyncio

from api_clients.sql_client import SQLClient
from threads.abstract_thread import AbstractThread
from tortoise_config import db_manager


class SQLClientThread(AbstractThread):
    """
    A threading client for working with a SQL database.

        Attributes:
            client_instance (SQLClient): An instance of the client for working with the SQL database.

        Args:
            currency_pair (str): The currency pair the client is working with.
            interval (int): The time interval between requests to the API.
    """

    def __init__(self, currency_pair: str, interval: int):
        super().__init__(currency_pair, interval)
        self.client_instance = SQLClient(currency_pair, interval)

    async def start_sql_client(self) -> None:
        await db_manager.initialize_db()
        await self.client_instance.start_polling()
        await db_manager.close_connection()

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_sql_client())
