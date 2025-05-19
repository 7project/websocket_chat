import pytest
from domain.values.users import Username
from domain.exceptions.users import UsernameTooShortException, UsernameTooLongException


def test_username_min_length():
    with pytest.raises(UsernameTooShortException):
        Username("ab")  # меньше 3 символов


def test_username_max_length():
    with pytest.raises(UsernameTooLongException):
        Username("a" * 33)  # больше 32 символов