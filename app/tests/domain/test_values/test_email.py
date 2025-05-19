import pytest
from domain.values.users import Email
from domain.exceptions.users import EmptyEmailException, InvalidEmailFormatException


def test_create_email_success():
    email = Email("test@example.com")
    assert email.as_generic_type() == "test@example.com"


def test_create_email_empty_value():
    with pytest.raises(EmptyEmailException):
        Email("")


def test_create_email_invalid_format():
    with pytest.raises(InvalidEmailFormatException):
        Email("invalid-email")