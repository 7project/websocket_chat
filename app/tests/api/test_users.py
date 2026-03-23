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
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_index_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "WebSocket Chat API"


@pytest.mark.asyncio
async def test_create_user_success(client):
    with patch("presentation.api.endpoints.users.UserRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_by_email = AsyncMock(return_value=None)
        mock_repo_class.return_value = mock_repo
        
        with patch("presentation.api.endpoints.users.create_mediator_with_session") as mock_mediator_factory:
            mock_mediator = AsyncMock()
            mock_user = MagicMock()
            mock_user.oid = "test-user-id"
            mock_user.email = MagicMock()
            mock_user.email.as_generic_type = MagicMock(return_value="test@example.com")
            mock_user.username = MagicMock()
            mock_user.username.as_generic_type = MagicMock(return_value="testuser")
            mock_mediator.send = AsyncMock(return_value=mock_user)
            mock_mediator_factory.return_value = mock_mediator
            
            with patch("presentation.api.endpoints.users.get_db") as mock_get_db:
                mock_db = AsyncMock()
                mock_db.commit = AsyncMock()
                mock_get_db.return_value = mock_db
                
                response = await client.post("/users/", json={
                    "email": "test@example.com",
                    "username": "testuser",
                    "password": "password123"
                })
                
                assert response.status_code == 200
                data = response.json()
                assert data["email"] == "test@example.com"
                assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_users_empty(client):
    with patch("presentation.api.endpoints.users.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.users.UserRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_repo = AsyncMock()
        mock_repo.get_all = AsyncMock(return_value=[])
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    with patch("presentation.api.endpoints.users.get_db") as mock_get_db, \
         patch("presentation.api.endpoints.users.UserRepository") as mock_repo_class:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id = AsyncMock(return_value=None)
        mock_repo_class.return_value = mock_repo
        
        response = await client.get("/users/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user_existing_email(client):
    with patch("presentation.api.endpoints.users.UserRepository") as mock_repo_class:
        mock_existing_user = MagicMock()
        mock_existing_user.id = "existing-id"
        mock_existing_user.email = "existing@example.com"
        mock_existing_user.username = "existinguser"
        
        mock_repo = MagicMock()
        mock_repo.get_by_email = AsyncMock(return_value=mock_existing_user)
        mock_repo_class.return_value = mock_repo
        
        with patch("presentation.api.endpoints.users.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value = mock_db
            
            response = await client.post("/users/", json={
                "email": "existing@example.com",
                "username": "newuser",
                "password": "password123"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "existing-id"
