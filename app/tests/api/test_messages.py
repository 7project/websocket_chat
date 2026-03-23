import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from presentation.api.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_chat_messages_empty(client):
    with patch("presentation.api.endpoints.messages.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.messages.MessageRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_repo = AsyncMock()
        mock_repo.get_by_chat = AsyncMock(return_value=[])
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/messages/chat/test-chat-id")
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_get_chat_messages_with_data(client):
    with patch("presentation.api.endpoints.messages.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.messages.MessageRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_message = MagicMock()
        mock_message.id = "msg-1"
        mock_message.chat_id = "chat-1"
        mock_message.sender_id = "user-1"
        mock_message.text = "Hello, World!"
        mock_message.timestamp = datetime(2024, 1, 1, 12, 0, 0)
        mock_message.is_read = False
        
        mock_repo = AsyncMock()
        mock_repo.get_by_chat = AsyncMock(return_value=[mock_message])
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/messages/chat/chat-1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "msg-1"
        assert data[0]["text"] == "Hello, World!"
        assert data[0]["sender_id"] == "user-1"
        assert data[0]["is_read"] is False


@pytest.mark.asyncio
async def test_get_chat_messages_multiple_messages(client):
    with patch("presentation.api.endpoints.messages.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.messages.MessageRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        messages = []
        for i in range(3):
            msg = MagicMock()
            msg.id = f"msg-{i}"
            msg.chat_id = "chat-1"
            msg.sender_id = f"user-{i}"
            msg.text = f"Message {i}"
            msg.timestamp = datetime(2024, 1, 1, 12, i, 0)
            msg.is_read = i > 0
            messages.append(msg)
        
        mock_repo = AsyncMock()
        mock_repo.get_by_chat = AsyncMock(return_value=messages)
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/messages/chat/chat-1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["is_read"] is False
        assert data[1]["is_read"] is True
        assert data[2]["is_read"] is True
