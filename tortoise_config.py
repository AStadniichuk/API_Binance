import threading

from tortoise import Tortoise

DATABASE_URL = "sqlite://db.sqlite3"


class Meta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DbManager(metaclass=Meta):
    """
        Class for managing database connections using the Tortoise ORM.

        This class ensures that there is only one instance of the database manager in the entire application.

        Attributes:
            initialized (bool): A flag indicating whether the database has been initialized.

        Methods:
            initialize_db(): Initializes the database connection if it has not yet been initialized.
            close_connection(): Closes the database connection if it has been initialized.
    """
    def __init__(self):
        self.initialized = False

    async def initialize_db(self) -> None:
        if not self.initialized:
            await Tortoise.init(
                db_url=DATABASE_URL,
                modules={"models": ["models.exchange_rate"]},
            )
            await Tortoise.generate_schemas()
            self.initialized = True

    async def close_connection(self) -> None:
        if self.initialized:
            await Tortoise.close_connections()


db_manager = DbManager()
