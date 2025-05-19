from domain.entities.chats import PrivateChat, GroupChat, ChatType
from domain.events.chats import ChatParticipantAddedEvent
from domain.values.chats import ChatTitle


def test_private_chat_creation():
    chat = PrivateChat(title=ChatTitle("Private Chat"), chat_type=ChatType.PRIVATE)
    assert chat.chat_type == ChatType.PRIVATE


def test_group_chat_creation():
    chat = GroupChat(title=ChatTitle("Group Chat"), chat_type=ChatType.GROUP)
    assert chat.chat_type == ChatType.GROUP


def test_chat_title_and_messages_initialization():
    title = ChatTitle("My Chat")
    chat = PrivateChat(title=title, chat_type=ChatType.PRIVATE)
    assert chat.title == title
    assert len(chat.messages) == 0

def test_add_participant_to_group_chat():
    chat = GroupChat(title=ChatTitle("Team Chat"), chat_type=ChatType.GROUP)
    chat.add_participant("user123")

    events = chat.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, ChatParticipantAddedEvent)
    assert event.chat_oid == chat.oid
    assert event.user_oid == "user123"