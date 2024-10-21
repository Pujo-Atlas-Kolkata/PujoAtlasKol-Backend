from typing import List, Callable, Dict, Optional

from .event import Event


class Registry:
    def __init__(self):
        self._handlers: Dict[str, List] = {}
        self._priorities: Dict[str, Dict[int, List[Callable[[Event], None]]]] = {}

    def add(self, event_name: str, handler: Callable[[Event], None], priority: Optional[int] = None) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
            self._priorities[event_name] = {}

        if not priority:
            if len(self._priorities[event_name]) > 0:
                priority = sorted(list(self._priorities[event_name].keys()))[-1] + 1
            else:
                priority = 1

        if priority not in self._priorities[event_name]:
            self._priorities[event_name][priority] = []

        self._priorities[event_name][priority].append(handler)

        priorities = sorted(list(self._priorities[event_name].keys()), reverse=True)

        self._handlers[event_name] = []

        for priority in priorities:
            handlers = self._priorities[event_name][priority]

            for handler in handlers:
                self._handlers[event_name].append(handler)

    def get(self, event: str) -> List[Callable[[Event], None]]:
        return self._handlers.get(event, [])
