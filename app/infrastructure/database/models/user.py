from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.users import User
from infrastructure.database.session import Base
from uuid import uuid4

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.database.models.chat import GroupChatModel
    from infrastructure.database.models.chat_participant import ChatParticipantModel
    from infrastructure.database.models.message import MessageModel

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    sent_messages: Mapped[list["MessageModel"]] = relationship(
        "MessageModel",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    created_group_chats: Mapped[list["GroupChatModel"]] = relationship(
        "GroupChatModel",
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    chat_memberships: Mapped[list["ChatParticipantModel"]] = relationship(
        "ChatParticipantModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            is_active=user.is_active
        )
