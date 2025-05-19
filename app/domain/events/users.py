from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    user_oid: str