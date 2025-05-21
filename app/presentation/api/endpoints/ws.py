from fastapi import APIRouter, WebSocket, Depends

from application.commands.create_chat import CreateChatCommand
from application.commands.send_message import SendMessageCommand
from application.mediator import Mediator
from application.dependencies import get_mediator
from manager import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        user_id: str,
        mediator: Mediator = Depends(get_mediator)
):
    await manager.connect(websocket, user_id, chat_id="default")

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "message":
                command = SendMessageCommand(**data)
                await mediator.send(command)

            elif data["type"] == "create_chat":
                command = CreateChatCommand(**data)
                await mediator.send(command)

            # elif data["type"] == "read":
            #     command = MarkMessageAsReadCommand(**data)
            #     await mediator.send(command)

    except Exception as e:
        print(e)
        manager.disconnect(websocket, user_id, chat_id="default")
