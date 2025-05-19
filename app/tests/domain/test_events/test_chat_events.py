from domain.events.chats import ChatParticipantAddedEvent


def test_chat_participant_added_event():
    event = ChatParticipantAddedEvent(chat_oid="chat_123", user_oid="user_456")
    assert event.chat_oid == "chat_123"
    assert event.user_oid == "user_456"