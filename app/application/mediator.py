from typing import TypeVar
from abc import ABC, abstractmethod
from typing import Callable, List, Dict
from collections import defaultdict

from application.exceptions.mediator import HandlerNotFoundException

CT = TypeVar("CT")
CR = TypeVar("CR")
ET = TypeVar("ET")


class AbstractMediator(ABC):
    @abstractmethod
    async def send(self, command: CT) -> CR:
        ...

    @abstractmethod
    async def publish(self, event: ET) -> None:
        ...


class Mediator(AbstractMediator):
    def __init__(self):
        self._command_handlers: Dict[type, Callable] = {}
        self._event_handlers: Dict[type, List[Callable]] = defaultdict(list)

    def register_handler(self, command_type, handler):
        self._command_handlers[command_type] = handler

    def subscribe(self, event_type, handler):
        self._event_handlers[event_type].append(handler)

    async def send(self, command: CT) -> CR:
        handler = self._command_handlers.get(type(command))
        if not handler:
            raise HandlerNotFoundException(f"Нет обработчика для {type(command)}")
        return await handler(command)

    async def publish(self, event: ET) -> None:
        for handler in self._event_handlers.get(type(event), []):
            await handler(event)
