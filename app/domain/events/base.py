import json
from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class BaseEvent(ABC):
    event_id: UUID = field(default_factory=uuid4, kw_only=True)

    def json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def parse_raw(cls, raw: str) -> "BaseEvent":
        return cls(**json.loads(raw))
