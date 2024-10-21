from dataclasses import dataclass
import datetime
import uuid
from typing import Optional


@dataclass
class Event:
    uuid: str = str(uuid.uuid4())
    timestamp: int = datetime.datetime.utcnow().timestamp()
    name: Optional[str] = None
