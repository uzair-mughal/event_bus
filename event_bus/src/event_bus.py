import asyncio
from typing import List, Optional
from event_bus.src.event import Event
from event_bus.src.event_handler import EventHandler


class EventBus:
    def __init__(self, handlers: Optional[List[EventHandler]] = None):
        self.__handlers = handlers if handlers is not None else []

    @property
    def handlers(self) -> List[EventHandler]:
        return self.__handlers

    def register_handler(self, handler: EventHandler):
        self.__handlers.append(handler)

    def unregister_handlers(self):
        self.__handlers = []

    async def broadcast(self, event: Event, topic: str = "") -> None:
        if topic == "":
            topic = event.name

        tasks = []
        for handler in self.handlers:
            if handler.is_subscribed_to_topic(topic):
                tasks.append(handler.handle(event=event, topic=topic))

        if len(tasks) > 0:
            await asyncio.gather(*tasks)
