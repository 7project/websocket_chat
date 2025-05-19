from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class EmptyEmailException(ApplicationException):
    @property
    def message(self):
        return 'Email не может быть пустым'


@dataclass(eq=False)
class InvalidEmailFormatException(ApplicationException):
    @property
    def message(self):
        return "Email имеет неправильный формат (ожидается '@')"


@dataclass(eq=False)
class EmptyUsernameException(ApplicationException):
    @property
    def message(self):
        return 'Username не может быть пустым'


@dataclass(eq=False)
class UsernameTooShortException(ApplicationException):
    @property
    def message(self):
        return 'Username слишком короткий (min 3 characters)'


@dataclass(eq=False)
class UsernameTooLongException(ApplicationException):
    @property
    def message(self):
        return 'Username слишком длинный (max 32 characters)'
