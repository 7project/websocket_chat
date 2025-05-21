from dataclasses import dataclass
from datetime import datetime
from application.mediator import Mediator
from domain.entities.messages import Message
from domain.events.messages import NewMessageReceivedEvent
from domain.values.messages import Text
from infrastructure.repositories.message import MessageRepository


@dataclass
class SendMessageCommand:
    chat_id: str
    sender_id: str
    text: str
    timestamp: datetime = datetime.utcnow()


@dataclass
class SendMessageCommandHandler:
    message_repo: MessageRepository
    mediator: Mediator

    async def handle(self, command: SendMessageCommand):
        message = Message(
            chat_id=command.chat_id,
            sender_id=command.sender_id,
            text=Text(command.text),
            created_at=command.timestamp
        )
        await self.message_repo.save(message)
        await self.mediator.publish(
            NewMessageReceivedEvent(
                message_oid=message.oid,
                message_text=message.text.as_generic_type(),
                chat_oid=message.chat_id,
                sender_id=message.sender_id
            )
        )
