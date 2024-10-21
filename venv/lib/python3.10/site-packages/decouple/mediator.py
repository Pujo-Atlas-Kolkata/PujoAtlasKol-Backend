from __future__ import annotations

from typing import Callable, Union, Any, Optional

from .event import Event
from .registry import Registry


class Mediator:
    def __init__(self,
                 registry: Registry = Registry()):
        self._registry = registry

    @staticmethod
    def _event_name(event: Union[Event, type]) -> str:
        if isinstance(event, type):
            return event.__name__
        elif isinstance(event, str):
            return event
        else:
            if event.name:
                return event.name
            else:
                return type(event).__name__

    def pub(self, event: Event) -> None:
        event_name = self._event_name(event)

        handlers = self._registry.get(event_name)

        for handler in handlers:
            handler(event)

    def add(self, event: Union[type, str], handler: Callable[[Any], None], priority: Optional[int] = None) -> Mediator:
        event_name = self._event_name(event)

        self._registry.add(event_name, handler, priority)

        return self
