from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from infrastructure.database.models.chat import ChatModel
from infrastructure.database.models.user import UserModel
from infrastructure.database.session import Base
from uuid import uuid4


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