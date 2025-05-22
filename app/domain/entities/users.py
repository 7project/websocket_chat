from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.users import UserCreatedEvent
from domain.values.users import Email, Username


@dataclass(eq=False)
class User(BaseEntity):
    email: Email
    username: Username
    is_active: bool = field(default=True)

    @classmethod
    def create_user(cls, email: Email, username: Username) -> 'User':
        user = cls(email=email, username=username)
        user.register_event(UserCreatedEvent(user_oid=user.oid))
        return user
