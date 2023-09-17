import functools
from typing import List
from task_runner import execute
from event_bus.src.event import Event
from event_bus.src.event_handler import EventHandler


class EventBus:
    def __init__(
        self,
        handlers: List[EventHandler] = [],
        tasks_limit: int = 1,
        retry_failures: bool = False,
        retry_limit: int = 1,
        retry_timeout: int = 5,
    ):
        self._tasks_limit = tasks_limit
        self._retry_failures = retry_failures
        self._retry_limit = retry_limit
        self._retry_timeout = retry_timeout
        self.register(handlers)

    def register(self, handlers: List[EventHandler]):
        self._handlers = handlers

    async def broadcast(self, event: Event, topic: str):
        tasks = []

        subscribed_handlers = list()
        for handler in self._handlers:
            if handler.is_subscribed_to_topic(topic):
                subscribed_handlers.append(type(handler).__name__)
                tasks.append(functools.partial(handler.handle, event))

        results = await execute(
            tasks=tasks,
            tasks_limit=self._tasks_limit,
            retry_failures=self._retry_failures,
            retry_timeout=self._retry_timeout,
            retry_limit=self._retry_limit,
        )

        return list(zip(subscribed_handlers, results))

    async def send(self, event: Event, topic: str):
        for handler in self._handlers:
            if handler.is_subscribed_to_topic(topic):
                try:
                    result = await handler.handle(event)
                    return (type(handler).__name__, result)
                except Exception as error:
                    return (type(handler).__name__, error)
