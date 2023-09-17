from pandas import DataFrame
from typing import List, Union
from abc import ABC, abstractmethod
from event_bus.src.event import Event


class EventHandler(ABC):
    def __init__(self, topics: List[str]):
        self._topics = topics

    @abstractmethod
    async def handle(self, event: Event, data: DataFrame):
        raise NotImplementedError

    def is_subscribed_to_topic(self, topic: str) -> bool:
        return topic in self._topics
