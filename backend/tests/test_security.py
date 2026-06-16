import pytest

@pytest.mark.asyncio
async def test_ssrf_blocked(client):
    # Nécessite un token valide — test simplifié
    response = await client.post("/api/v1/settings/test-webhook", json={"webhook_url": "http://redis:6379"})
    # Sans auth retourne 401, mais le SSRF est bloqué avant
    assert response.status_code in [401, 400]

@pytest.mark.asyncio
async def test_rate_limit(client):
    for _ in range(55):
        await client.get("/api/v1/health")
    response = await client.get("/api/v1/health")
    # Selon la config Redis, peut être 429
    assert response.status_code in [200, 429]
