import pytest
from application.mediator import Mediator
from application.exceptions.mediator import HandlerNotFoundException


@pytest.fixture
def mediator():
    return Mediator()


@pytest.mark.asyncio
async def test_mediator_send_without_handler_raises_exception(mediator):
    class DummyCommand:
        pass
    
    with pytest.raises(HandlerNotFoundException):
        await mediator.send(DummyCommand())


@pytest.mark.asyncio
async def test_mediator_send_with_handler_returns_result(mediator):
    class DummyCommand:
        def __init__(self, value):
            self.value = value

    async def handler(cmd):
        return cmd.value * 2

    mediator.register_handler(DummyCommand, handler)
    
    result = await mediator.send(DummyCommand(5))
    assert result == 10


@pytest.mark.asyncio
async def test_mediator_publish_calls_subscribers(mediator):
    class DummyEvent:
        def __init__(self, message):
            self.message = message

    called = []
    
    async def subscriber1(event):
        called.append(("sub1", event.message))
    
    async def subscriber2(event):
        called.append(("sub2", event.message))
    
    mediator.subscribe(DummyEvent, subscriber1)
    mediator.subscribe(DummyEvent, subscriber2)
    
    await mediator.publish(DummyEvent("test"))
    
    assert len(called) == 2
    assert ("sub1", "test") in called
    assert ("sub2", "test") in called


@pytest.mark.asyncio
async def test_mediator_publish_without_subscribers_no_error(mediator):
    class UnknownEvent:
        pass
    
    await mediator.publish(UnknownEvent())


def test_mediator_register_handler_overwrites_existing(mediator):
    class Command:
        pass
    
    async def handler1(cmd):
        return 1
    
    async def handler2(cmd):
        return 2
    
    mediator.register_handler(Command, handler1)
    mediator.register_handler(Command, handler2)
    
    assert mediator._command_handlers[Command] == handler2


def test_mediator_subscribe_multiple_handlers_same_event(mediator):
    class Event:
        pass
    
    async def h1(e): pass
    async def h2(e): pass
    
    mediator.subscribe(Event, h1)
    mediator.subscribe(Event, h2)
    
    assert len(mediator._event_handlers[Event]) == 2
