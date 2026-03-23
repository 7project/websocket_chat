from datetime import datetime
from domain.entities.messages import Message
from domain.values.messages import Text


def test_message_creation():
    text = Text("Hello, World!")
    message = Message(chat_id="chat123", sender_id="user456", text=text)
    
    assert message.chat_id == "chat123"
    assert message.sender_id == "user456"
    assert message.text == text
    assert message.is_read is False


def test_message_has_oid():
    text = Text("Test message")
    message = Message(chat_id="chat1", sender_id="user1", text=text)
    
    assert message.oid is not None
    assert len(message.oid) == 36


def test_message_timestamp_default():
    text = Text("Test")
    before = datetime.utcnow()
    message = Message(chat_id="chat1", sender_id="user1", text=text)
    after = datetime.utcnow()
    
    assert before <= message.timestamp <= after


def test_message_custom_timestamp():
    custom_time = datetime(2024, 1, 1, 12, 0, 0)
    text = Text("Test")
    message = Message(chat_id="chat1", sender_id="user1", text=text, timestamp=custom_time)
    
    assert message.timestamp == custom_time


def test_message_mark_as_read():
    text = Text("Test")
    message = Message(chat_id="chat1", sender_id="user1", text=text)
    
    assert message.is_read is False
    message.is_read = True
    assert message.is_read is True


def test_message_text_as_generic_type():
    text = Text("Hello")
    message = Message(chat_id="chat1", sender_id="user1", text=text)
    
    assert message.text.as_generic_type() == "Hello"
