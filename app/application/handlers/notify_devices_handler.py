from domain.events.messages import NewMessageReceivedEvent
from manager import manager

async def notify_devices_handler(event: NewMessageReceivedEvent):
    await manager.broadcast_to_chat(event.chat_oid, {
        "type": "message",
        "id": event.message_oid,
        "chat_id": event.chat_oid,
        "sender_id": event.sender_id,
        "text": event.message_text
    })
