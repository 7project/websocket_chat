from domain.exceptions.base import ApplicationException
from dataclasses import dataclass

@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    ...


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Слишком длинный текст сообщения "{self.text[:255]}..."'