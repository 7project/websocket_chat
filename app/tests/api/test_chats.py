import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from presentation.api.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_chat_success(client):
    with patch("presentation.api.endpoints.chats.create_mediator_with_session") as mock_mediator_factory, \
         patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_repo_class:
        
        mock_db = AsyncMock()
        mock_db.commit = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_mediator = AsyncMock()
        mock_chat = MagicMock()
        mock_chat.oid = "test-chat-id"
        mock_mediator.send = AsyncMock(return_value=mock_chat)
        mock_mediator_factory.return_value = mock_mediator
        
        mock_saved_chat = MagicMock()
        mock_saved_chat.id = "test-chat-id"
        mock_saved_chat.title = "Test Chat"
        mock_saved_chat.type = "group"
        mock_participant = MagicMock()
        mock_participant.user_id = "user1"
        mock_saved_chat.participants = [mock_participant]
        
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_saved_chat)
        mock_repo_class.return_value = mock_repo
        
        response = await client.post("/chats/", json={
            "title": "Test Chat",
            "type": "group",
            "creator_id": "user1",
            "participants": ["user1"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Chat"
        assert data["type"] == "group"


@pytest.mark.asyncio
async def test_create_chat_without_creator_id_returns_400(client):
    response = await client.post("/chats/", json={
        "title": "Test Chat",
        "type": "group",
        "creator_id": None,
        "participants": []
    })
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_chats_empty(client):
    with patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_repo = AsyncMock()
        mock_repo.get_all = AsyncMock(return_value=[])
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/chats/")
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_get_chat_not_found(client):
    with patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id = AsyncMock(return_value=None)
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/chats/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_chats_with_data(client):
    with patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_chat = MagicMock()
        mock_chat.id = "chat-1"
        mock_chat.title = "Test Chat"
        mock_chat.type = "group"
        mock_participant = MagicMock()
        mock_participant.user_id = "user-1"
        mock_chat.participants = [mock_participant]
        
        mock_repo = AsyncMock()
        mock_repo.get_all = AsyncMock(return_value=[mock_chat])
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/chats/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "chat-1"
        assert data[0]["title"] == "Test Chat"


@pytest.mark.asyncio
async def test_add_participant_success(client):
    with patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_chat_repo_class, \
         patch("presentation.api.endpoints.chats.UserRepository") as mock_user_repo_class:
        
        mock_db = AsyncMock()
        mock_db.commit = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_chat = MagicMock()
        mock_chat.id = "chat-1"
        
        mock_chat_repo = MagicMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=mock_chat)
        mock_chat_repo.add_participant = AsyncMock(return_value=True)
        mock_chat_repo_class.return_value = mock_chat_repo
        
        mock_user = MagicMock()
        mock_user.id = "user-1"
        
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
        mock_user_repo_class.return_value = mock_user_repo
        
        mock_saved_chat = MagicMock()
        mock_saved_chat.id = "chat-1"
        mock_saved_chat.title = "Test Chat"
        mock_saved_chat.type = "group"
        mock_saved_chat.participants = [MagicMock(user_id="user-1")]
        mock_chat_repo.get_by_id = AsyncMock(return_value=mock_saved_chat)
        
        response = await client.post("/chats/chat-1/participants", json={
            "user_id": "user-1"
        })
        
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_participants(client):
    with patch("presentation.api.endpoints.chats.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.chats.ChatRepository") as mock_chat_repo_class, \
         patch("presentation.api.endpoints.chats.UserRepository") as mock_user_repo_class:
        
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_participant = MagicMock()
        mock_participant.user_id = "user-1"
        
        mock_chat = MagicMock()
        mock_chat.id = "chat-1"
        mock_chat.participants = [mock_participant]
        
        mock_chat_repo = MagicMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=mock_chat)
        mock_chat_repo_class.return_value = mock_chat_repo
        
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
        mock_user_repo_class.return_value = mock_user_repo
        
        response = await client.get("/chats/chat-1/participants")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_id"] == "user-1"
