import pytest
from domain.values.chats import ChatTitle
from domain.exceptions.chats import EmptyTextException, TitleTooLongException


def test_valid_chat_title():
    title = ChatTitle("Valid title")
    assert title.as_generic_type() == "Valid title"


def test_empty_chat_title_raises_exception():
    with pytest.raises(EmptyTextException):
        ChatTitle("")


def test_long_chat_title_raises_exception():
    with pytest.raises(TitleTooLongException):
        ChatTitle("x" * 256)