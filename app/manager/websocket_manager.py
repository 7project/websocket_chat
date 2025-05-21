from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, dict[str, list[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, user_id: str, chat_id: str):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        if user_id not in self.active_connections[chat_id]:
            self.active_connections[chat_id][user_id] = []
        self.active_connections[chat_id][user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str, chat_id: str):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            sockets = self.active_connections[chat_id][user_id]
            if websocket in sockets:
                sockets.remove(websocket)
                if not sockets:
                    del self.active_connections[chat_id][user_id]
                if not self.active_connections[chat_id]:
                    del self.active_connections[chat_id]

    async def broadcast_to_chat(self, chat_id: str, message: dict):
        if chat_id in self.active_connections:
            for sockets in self.active_connections[chat_id].values():
                for socket in sockets:
                    await socket.send_json(message)

    async def send_to_user(self, chat_id: str, user_id: str, message: dict):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            for socket in self.active_connections[chat_id][user_id]:
                await socket.send_json(message)
