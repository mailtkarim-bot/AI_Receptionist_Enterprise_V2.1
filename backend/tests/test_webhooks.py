import pytest

@pytest.mark.asyncio
async def test_vapi_webhook_rejects_invalid_signature(client):
    response = await client.post("/api/v1/webhooks/vapi", json={"event": "test"}, headers={"X-Vapi-Signature": "invalid"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_twilio_webhook_rejects_invalid_signature(client):
    response = await client.post("/api/v1/webhooks/twilio/sms", data={"MessageSid": "test"}, headers={"X-Twilio-Signature": "invalid"})
    assert response.status_code == 401
