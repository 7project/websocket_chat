from datetime import datetime
from domain.entities.read_receipts import ReadReceipt


def test_read_receipt_created_at():
    receipt = ReadReceipt(message_oid="msg123", reader_oid="user456")
    assert receipt.created_at.date() == datetime.today().date()