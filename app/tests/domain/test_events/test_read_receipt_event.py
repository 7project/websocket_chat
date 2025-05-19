from domain.events.read_receipts import MessageReadEvent


def test_message_read_event_has_correct_fields():
    event = MessageReadEvent(message_oid="msg123", reader_oid="user456")
    assert event.message_oid == "msg123"
    assert event.reader_oid == "user456"