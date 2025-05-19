from datetime import datetime
from domain.entities.users import User
from domain.values.users import Email, Username


def test_user_activate():
    email = Email("test@example.com")
    username = Username("john_doe")
    user = User(email=email, username=username, is_active=False)
    assert not user.is_active

    user.is_active = True
    assert user.is_active


def test_create_user_success():
    email = Email("test@example.com")
    username = Username("john_doe")
    user = User(email=email, username=username, is_active=False)

    assert user.email == email
    assert user.username == username
    assert user.created_at.date() == datetime.today().date()
    assert not user.is_active