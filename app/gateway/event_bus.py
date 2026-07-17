from collections import defaultdict
from collections.abc import Callable, Awaitable
from typing import Any

EventHandler = Callable[[Any], Awaitable[None]]

class EventBus:
    def __init__(self):
        self._handlers: dict[type, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: EventHandler):
        self._handlers[event_type].append(handler)

    async def publish(self, event):
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            await handler(event)
