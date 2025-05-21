from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.chat_participant import ChatParticipantModel
from infrastructure.database.models.message import MessageModel
from infrastructure.database.models.user import UserModel
from infrastructure.database.session import Base
from uuid import uuid4


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    messages: Mapped[list["MessageModel"]] = relationship(
        "MessageModel",
        back_populates="chat",
        cascade="all, delete-orphan"
    )

    participants: Mapped[list["ChatParticipantModel"]] = relationship(
        "ChatParticipantModel",
        back_populates="chat",
        cascade="all, delete-orphan"
    )


class GroupChatModel(ChatModel):
    __tablename__ = "group_chats"

    id: Mapped[str] = mapped_column(String, ForeignKey("chats.id"), primary_key=True)
    creator_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)

    creator: Mapped["UserModel"] = relationship("UserModel", back_populates="created_group_chats")