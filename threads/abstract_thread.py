import threading

from abc import ABC, abstractmethod
from typing import Type


class AbstractThread(threading.Thread, ABC):
    currency_pair: str
    interval: int

    def __init__(self, currency_pair: str, interval: int):
        super().__init__()
        self.currency_pair = currency_pair
        self.interval = interval
        self.client_instance: Type = None

    @abstractmethod
    def run(self):
        pass
