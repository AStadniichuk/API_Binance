import asyncio

from api_clients.sql_client import SQLClient
from threads.abstract_thread import AbstractThread
from tortoise_config import db_manager


class SQLClientThread(AbstractThread):
    def __init__(self, currency_pair, interval):
        super().__init__(currency_pair, interval)
        self.client_instance = SQLClient(currency_pair, interval)

    async def start_sql_client(self):
        await db_manager.initialize_db()
        await self.client_instance.start_polling()
        await db_manager.close_connection()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_sql_client())
