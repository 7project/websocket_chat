from manager import manager
from domain.events.chats import NewChatCreated


async def chat_created_handler(event: NewChatCreated):
    await manager.broadcast_to_all({
        "type": "new_chat",
        "chat_id": event.chat_oid,
        "title": event.chat_title
    })
