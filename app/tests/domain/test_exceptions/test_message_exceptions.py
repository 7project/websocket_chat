from domain.exceptions.messages import EmptyTextException


def test_empty_text_exception():
    try:
        raise EmptyTextException()
    except EmptyTextException as e:
        assert str(e.message) == "Текст не может быть пустым"