import pytest

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/api/v1/auth/register", json={
        "name": "Test Business",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "phone": "+1234567890"
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Test Business",
        "email": "login@example.com",
        "password": "SecurePass123!",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "SecurePass123!",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_logout_revokes_token(client):
    reg = await client.post("/api/v1/auth/register", json={
        "name": "Test",
        "email": "logout@example.com",
        "password": "SecurePass123!",
    })
    token = reg.json()["access_token"]
    await client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 401
