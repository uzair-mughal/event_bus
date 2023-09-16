from abc import ABC, abstractmethod
from typing import List
from event_bus.src.event import Event


class EventHandler(ABC):
    def __init__(self, topics: List[str]):
        self.__topics = topics

    @property
    def topics(self):
        return self.__topics

    @abstractmethod
    async def handle(self, event: Event, topic: str) -> None:
        raise NotImplementedError

    def is_subscribed_to_topic(self, topic: str) -> bool:
        return topic in self.topics
