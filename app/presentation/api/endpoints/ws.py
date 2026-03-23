import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from application.commands.create_chat import CreateChatCommand
from application.commands.send_message import SendMessageCommand
from application.dependencies import create_mediator_with_session
from infrastructure.database.session import AsyncSessionLocal
from infrastructure.repositories.chat import ChatRepository
from manager import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    
    chat_id = "default"
    if chat_id not in manager.active_connections:
        manager.active_connections[chat_id] = {}
    if user_id not in manager.active_connections[chat_id]:
        manager.active_connections[chat_id][user_id] = []
    manager.active_connections[chat_id][user_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            async with AsyncSessionLocal() as session:
                mediator = create_mediator_with_session(session)
                chat_repo = ChatRepository(session)
                
                if message_type == "message":
                    msg_chat_id = data.get("chat_id")
                    text = data.get("text")
                    
                    if not msg_chat_id or not text:
                        await websocket.send_json({"type": "error", "message": "chat_id and text are required"})
                        continue
                    
                    command = SendMessageCommand(
                        chat_id=msg_chat_id,
                        sender_id=user_id,
                        text=text
                    )
                    await mediator.send(command)
                    await session.commit()

                elif message_type == "create_chat":
                    title = data.get("title")
                    participants = data.get("participants", [user_id])
                    
                    if not title:
                        await websocket.send_json({"type": "error", "message": "title is required"})
                        continue
                    
                    command = CreateChatCommand(
                        title=title,
                        creator_id=user_id,
                        participants=participants
                    )
                    chat = await mediator.send(command)
                    await session.commit()
                    
                    try:
                        await manager.broadcast_to_all({
                            "type": "new_chat",
                            "id": chat.oid,
                            "title": chat.title.as_generic_type()
                        })
                    except Exception:
                        pass

                elif message_type == "join_chat":
                    new_chat_id = data.get("chat_id")
                    if not new_chat_id:
                        await websocket.send_json({"type": "error", "message": "chat_id is required"})
                        continue
                    
                    if chat_id in manager.active_connections and user_id in manager.active_connections[chat_id]:
                        if websocket in manager.active_connections[chat_id][user_id]:
                            manager.active_connections[chat_id][user_id].remove(websocket)
                    
                    if new_chat_id not in manager.active_connections:
                        manager.active_connections[new_chat_id] = {}
                    if user_id not in manager.active_connections[new_chat_id]:
                        manager.active_connections[new_chat_id][user_id] = []
                    manager.active_connections[new_chat_id][user_id].append(websocket)
                    chat_id = new_chat_id
                    
                    await websocket.send_json({"type": "joined", "chat_id": new_chat_id})

                elif message_type == "add_participant":
                    target_chat_id = data.get("chat_id")
                    new_user_id = data.get("user_id")
                    
                    if not target_chat_id or not new_user_id:
                        await websocket.send_json({"type": "error", "message": "chat_id and user_id are required"})
                        continue
                    
                    added = await chat_repo.add_participant(target_chat_id, new_user_id)
                    await session.commit()
                    
                    if added:
                        await websocket.send_json({
                            "type": "participant_added",
                            "chat_id": target_chat_id,
                            "user_id": new_user_id
                        })
                    else:
                        await websocket.send_json({"type": "error", "message": "User already in chat"})

                elif message_type == "ping":
                    await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: user={user_id}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if chat_id in manager.active_connections and user_id in manager.active_connections[chat_id]:
            if websocket in manager.active_connections[chat_id][user_id]:
                manager.active_connections[chat_id][user_id].remove(websocket)
