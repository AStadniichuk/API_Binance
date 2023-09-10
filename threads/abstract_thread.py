import threading

from abc import ABC, abstractmethod
from typing import Type

from api_clients.abstract_client import AbstractAPIClient


class AbstractThread(threading.Thread, ABC):
    """
        An abstract base class for creating client threads.

        Attributes:
            currency_pair (str): The currency pair the client is working with.
            interval (int): The time interval between requests to the API.
            client_instance (Type[AbstractAPIClient]): An instance of the client for working with a specific API.

        Args:
            currency_pair (str): The currency pair the client is working with.
            interval (int): The time interval between requests to the API.
        """
    currency_pair: str
    interval: int

    def __init__(self, currency_pair: str, interval: int):
        super().__init__()
        self.currency_pair = currency_pair
        self.interval = interval
        self.client_instance: Type[AbstractAPIClient] | None = None

    @abstractmethod
    def run(self) -> None:
        pass
