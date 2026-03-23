from domain.events.messages import NewMessageReceivedEvent


def test_new_message_event_data():
    event = NewMessageReceivedEvent(
        message_oid="msg_123",
        message_text="Hello",
        chat_oid="chat_456",
        sender_id="user_789"
    )
    assert event.message_oid == "msg_123"
    assert event.message_text == "Hello"
    assert event.chat_oid == "chat_456"
    assert event.sender_id == "user_789"