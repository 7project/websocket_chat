from dataclasses import dataclass

from domain.values.base import BaseValueObject
from domain.exceptions.users import EmptyEmailException, InvalidEmailFormatException, EmptyUsernameException, \
    UsernameTooShortException, UsernameTooLongException


@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyEmailException()

        if "@" not in self.value:
            raise InvalidEmailFormatException()

    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Username(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyUsernameException()

        if len(self.value) < 3:
            raise UsernameTooShortException()

        if len(self.value) > 32:
            raise UsernameTooLongException()

    def as_generic_type(self) -> str:
        return self.value