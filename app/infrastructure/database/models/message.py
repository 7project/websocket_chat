from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.messages import Message
from infrastructure.database.session import Base
from uuid import uuid4

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.database.models.chat import ChatModel
    from infrastructure.database.models.user import UserModel


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    chat_id: Mapped[str] = mapped_column(String, ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    chat: Mapped["ChatModel"] = relationship("ChatModel", back_populates="messages")
    sender: Mapped["UserModel"] = relationship("UserModel", back_populates="sent_messages")

    @classmethod
    def from_entity(cls, message: "Message") -> "MessageModel":
        return cls(
            id=message.oid,
            chat_id=message.chat_id,
            sender_id=message.sender_id,
            text=message.text.as_generic_type(),
            timestamp=message.timestamp,
            is_read=message.is_read
        )
