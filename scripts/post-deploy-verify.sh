#!/bin/bash
set -euo pipefail

BASE_URL="${API_URL:-https://api.aireceptionist.example.com}"

echo "=== POST-DEPLOYMENT VERIFICATION ==="

STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/health")
[[ "$STATUS" == "200" ]] || { echo "Health check failed: $STATUS"; exit 1; }
echo "Health: OK"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/metrics")
[[ "$STATUS" == "403" ]] || { echo "Metrics not protected: $STATUS"; exit 1; }
echo "Metrics protected: OK"

for i in $(seq 1 11); do
  curl -sf -X POST "$BASE_URL/api/v1/auth/login"     -H "Content-Type: application/json"     -d '{"email":"test@test.com","password":"wrong"}' > /dev/null || true
done
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/auth/login"   -H "Content-Type: application/json"   -d '{"email":"test@test.com","password":"wrong"}')
[[ "$STATUS" == "429" ]] || { echo "Brute force not blocked: $STATUS"; exit 1; }
echo "Brute force protection: OK"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/settings/test-webhook"   -H "Authorization: Bearer $TEST_TOKEN"   -H "Content-Type: application/json"   -d '{"webhook_url":"http://redis:6379"}')
[[ "$STATUS" == "400" ]] || { echo "SSRF not blocked: $STATUS"; exit 1; }
echo "SSRF protection: OK"

TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login"   -H "Content-Type: application/json"   -d "{"email":"$TEST_EMAIL","password":"$TEST_PASSWORD"}" | jq -r .access_token)
curl -s -X POST "$BASE_URL/api/v1/auth/logout" -H "Authorization: Bearer $TOKEN" > /dev/null
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/auth/me"   -H "Authorization: Bearer $TOKEN")
[[ "$STATUS" == "401" ]] || { echo "Token not revoked after logout: $STATUS"; exit 1; }
echo "Token revocation: OK"

echo "=== ALL CHECKS PASSED ==="
