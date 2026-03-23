import pytest
from unittest.mock import AsyncMock, MagicMock
from application.commands.create_user import CreateUserCommand, CreateUserCommandHandler
from application.commands.create_chat import CreateChatCommand, CreateChatCommandHandler
from application.commands.send_message import SendMessageCommand, SendMessageCommandHandler
from domain.values.users import Email, Username
from domain.values.chats import ChatTitle
from domain.values.messages import Text


@pytest.mark.asyncio
async def test_create_user_command_handler():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = CreateUserCommandHandler(user_repo=mock_repo, mediator=mock_mediator)
    command = CreateUserCommand(email="test@example.com", username="testuser")
    
    user = await handler.handle(command)
    
    mock_repo.save.assert_called_once()
    assert user.email.as_generic_type() == "test@example.com"
    assert user.username.as_generic_type() == "testuser"


@pytest.mark.asyncio
async def test_create_chat_command_handler():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = CreateChatCommandHandler(chat_repo=mock_repo, mediator=mock_mediator)
    command = CreateChatCommand(
        title="Test Chat",
        creator_id="user123",
        participants=["user123", "user456"]
    )
    
    chat = await handler.handle(command)
    
    mock_repo.save.assert_called_once()
    mock_mediator.publish.assert_called_once()
    assert chat.title.as_generic_type() == "Test Chat"
    assert "user123" in chat.participants
    assert "user456" in chat.participants


@pytest.mark.asyncio
async def test_send_message_command_handler():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = SendMessageCommandHandler(message_repo=mock_repo, mediator=mock_mediator)
    command = SendMessageCommand(
        chat_id="chat123",
        sender_id="user456",
        text="Hello, World!"
    )
    
    await handler.handle(command)
    
    mock_repo.save.assert_called_once()
    mock_mediator.publish.assert_called_once()
    published_event = mock_mediator.publish.call_args[0][0]
    assert published_event.message_text == "Hello, World!"
    assert published_event.chat_oid == "chat123"
    assert published_event.sender_id == "user456"


@pytest.mark.asyncio
async def test_create_user_command_generates_oid():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = CreateUserCommandHandler(user_repo=mock_repo, mediator=mock_mediator)
    command = CreateUserCommand(email="test@example.com", username="testuser")
    
    user = await handler.handle(command)
    
    assert user.oid is not None
    assert len(user.oid) == 36


@pytest.mark.asyncio
async def test_create_chat_command_generates_oid():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = CreateChatCommandHandler(chat_repo=mock_repo, mediator=mock_mediator)
    command = CreateChatCommand(
        title="Test Chat",
        creator_id="user123",
        participants=["user123"]
    )
    
    chat = await handler.handle(command)
    
    assert chat.oid is not None
    assert len(chat.oid) == 36


@pytest.mark.asyncio
async def test_send_message_command_generates_oid():
    mock_repo = AsyncMock()
    mock_mediator = AsyncMock()
    
    handler = SendMessageCommandHandler(message_repo=mock_repo, mediator=mock_mediator)
    command = SendMessageCommand(
        chat_id="chat123",
        sender_id="user456",
        text="Hello!"
    )
    
    mock_repo.save.side_effect = lambda msg: msg
    
    await handler.handle(command)
    
    saved_message = mock_repo.save.call_args[0][0]
    assert saved_message.oid is not None
