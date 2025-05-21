from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.chat import ChatModel
from infrastructure.database.models.user import UserModel
from infrastructure.database.session import Base

class ChatParticipantModel(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[str] = mapped_column(String, ForeignKey("chats.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), primary_key=True)

    chat: Mapped["ChatModel"] = relationship("ChatModel", back_populates="participants")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="chat_memberships")
