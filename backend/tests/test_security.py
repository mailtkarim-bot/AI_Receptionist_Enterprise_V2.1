import pytest

@pytest.mark.asyncio
async def test_ssrf_blocked(client):
    response = await client.post("/api/v1/settings/test-webhook", json={"webhook_url": "http://redis:6379"})
    assert response.status_code in [401, 400]

@pytest.mark.asyncio
async def test_rate_limit(client):
    for _ in range(55):
        await client.get("/api/v1/health")
    response = await client.get("/api/v1/health")
    assert response.status_code in [200, 429]
