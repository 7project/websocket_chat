from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database.session import Base

from infrastructure.database.models.message import MessageModel
from infrastructure.database.models.user import UserModel


class ReadReceiptModel(Base):
    __tablename__ = "read_receipts"

    message_id: Mapped[str] = mapped_column(String, ForeignKey("messages.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), primary_key=True)
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    message: Mapped["MessageModel"] = relationship("MessageModel", back_populates="read_receipts")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="read_receipts")
