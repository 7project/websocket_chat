from enum import Enum
from dataclasses import dataclass
from domain.values.base import BaseValueObject
from domain.exceptions.chats import EmptyTextException, TitleTooLongException

class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


@dataclass(frozen=True)
class ChatTitle(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)