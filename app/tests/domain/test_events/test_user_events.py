from domain.events.users import UserCreatedEvent


def test_user_created_event():
    event = UserCreatedEvent(user_oid="abc123")
    assert event.user_oid == "abc123"