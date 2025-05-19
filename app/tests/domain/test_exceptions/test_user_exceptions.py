from domain.exceptions.users import (
    EmptyEmailException,
    InvalidEmailFormatException,
    EmptyUsernameException,
    UsernameTooShortException,
    UsernameTooLongException
)


def test_empty_email_exception_message():
    try:
        raise EmptyEmailException()
    except EmptyEmailException as e:
        assert str(e.message) == "Email не может быть пустым"


def test_invalid_email_exception_message():
    try:
        raise InvalidEmailFormatException()
    except InvalidEmailFormatException as e:
        assert str(e.message) == "Email имеет неправильный формат (ожидается '@')"


def test_empty_username_exception_message():
    try:
        raise EmptyUsernameException()
    except EmptyUsernameException as e:
        assert str(e.message) == "Username не может быть пустым"


def test_username_too_short_exception_message():
    try:
        raise UsernameTooShortException()
    except UsernameTooShortException as e:
        assert str(e.message) == "Username слишком короткий (min 3 characters)"


def test_username_too_long_exception_message():
    try:
        raise UsernameTooLongException()
    except UsernameTooLongException as e:
        assert str(e.message) == "Username слишком длинный (max 32 characters)"