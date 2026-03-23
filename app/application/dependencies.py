from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.commands.create_chat import CreateChatCommandHandler, CreateChatCommand
from application.commands.create_user import CreateUserCommandHandler, CreateUserCommand
from application.commands.send_message import SendMessageCommandHandler, SendMessageCommand
from application.handlers.chat_created_handler import chat_created_handler
from application.handlers.notify_devices_handler import notify_devices_handler
from application.mediator import Mediator
from domain.events.chats import NewChatCreated
from domain.events.messages import NewMessageReceivedEvent
from infrastructure.database.session import get_db, AsyncSessionLocal
from infrastructure.repositories.chat import ChatRepository
from infrastructure.repositories.message import MessageRepository
from infrastructure.repositories.user import UserRepository


def get_mediator(db: AsyncSession = Depends(get_db)):
    message_repo = MessageRepository(db)
    chat_repo = ChatRepository(db)
    user_repo = UserRepository(db)
    mediator = Mediator()

    send_message_handler = SendMessageCommandHandler(message_repo, mediator)
    create_chat_handler = CreateChatCommandHandler(chat_repo, mediator)
    create_user_handler = CreateUserCommandHandler(user_repo, mediator)

    mediator.register_handler(SendMessageCommand, send_message_handler.handle)
    mediator.register_handler(CreateChatCommand, create_chat_handler.handle)
    mediator.register_handler(CreateUserCommand, create_user_handler.handle)

    mediator.subscribe(NewMessageReceivedEvent, notify_devices_handler)
    mediator.subscribe(NewChatCreated, chat_created_handler)

    return mediator


def create_mediator_with_session(session: AsyncSession) -> Mediator:
    message_repo = MessageRepository(session)
    chat_repo = ChatRepository(session)
    user_repo = UserRepository(session)
    mediator = Mediator()
    
    send_message_handler = SendMessageCommandHandler(message_repo, mediator)
    create_chat_handler = CreateChatCommandHandler(chat_repo, mediator)
    create_user_handler = CreateUserCommandHandler(user_repo, mediator)

    mediator.register_handler(SendMessageCommand, send_message_handler.handle)
    mediator.register_handler(CreateChatCommand, create_chat_handler.handle)
    mediator.register_handler(CreateUserCommand, create_user_handler.handle)

    mediator.subscribe(NewMessageReceivedEvent, notify_devices_handler)
    mediator.subscribe(NewChatCreated, chat_created_handler)

    return mediator