from domain.exceptions.chats import TitleTooLongException


# def test_title_too_long():
#     try:
#         raise TitleTooLongException("a" * 256)
#     except TitleTooLongException as e:
#         assert str(e.message) == f'Слишком длинный текст сообщения "{e.text[:255]}..."'
