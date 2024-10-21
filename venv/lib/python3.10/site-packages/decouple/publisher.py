from abc import ABC
from typing import Optional

from .event import Event
from .mediator import Mediator


class Publisher(ABC):
    def __init__(self,
                 mediator: Optional[Mediator] = None):
        self._mediator = mediator

    def pub(self, event: Event):
        self._mediator.pub(event)
