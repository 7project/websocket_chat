from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.events.read_receipts import MessageReadEvent


@dataclass(eq=False)
class ReadReceipt(BaseEntity):
    message_oid: str
    reader_oid: str
    read_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def mark_as_read(cls, message_oid: str, reader_oid: str) -> 'ReadReceipt':
        receipt = cls(message_oid=message_oid, reader_oid=reader_oid)
        receipt.register_event(MessageReadEvent(
            message_oid=message_oid,
            reader_oid=reader_oid
        ))
        return receipt