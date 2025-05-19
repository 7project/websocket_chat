import pytest
from domain.values.messages import Text
from domain.exceptions.messages import EmptyTextException


def test_text_valid():
    text = Text("Hello world")
    assert text.as_generic_type() == "Hello world"


def test_text_empty_raises_exception():
    with pytest.raises(EmptyTextException):
        Text("")


def test_text_with_spaces_allowed():
    text = Text("   spaced text   ")
    assert text.as_generic_type() == "   spaced text   "