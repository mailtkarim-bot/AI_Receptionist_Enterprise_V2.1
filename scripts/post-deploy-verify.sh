#!/bin/bash
# =============================================================================
# Post-deployment verification
# =============================================================================
set -euo pipefail

BASE_URL="${API_URL:-https://api.aireceptionist.example.com}"

echo "=== VÉRIFICATION POST-DÉPLOIEMENT ==="

# 1. Health check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/health")
[[ "$STATUS" == "200" ]] || { echo "❌ Health check failed: $STATUS"; exit 1; }
echo "✅ Health: OK"

# 2. Metrics protected
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/metrics")
[[ "$STATUS" == "403" ]] || { echo "❌ Metrics non protégées: $STATUS"; exit 1; }
echo "✅ Metrics protégées: OK"

# 3. Brute force
for i in $(seq 1 11); do
  curl -sf -X POST "$BASE_URL/api/v1/auth/login"     -H "Content-Type: application/json"     -d '{"email":"test@test.com","password":"wrong"}' > /dev/null || true
done
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/auth/login"   -H "Content-Type: application/json"   -d '{"email":"test@test.com","password":"wrong"}')
[[ "$STATUS" == "429" ]] || { echo "❌ Brute force non bloqué: $STATUS"; exit 1; }
echo "✅ Brute force protection: OK"

# 4. SSRF
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/settings/test-webhook"   -H "Authorization: Bearer $TEST_TOKEN"   -H "Content-Type: application/json"   -d '{"webhook_url":"http://redis:6379"}')
[[ "$STATUS" == "400" ]] || { echo "❌ SSRF non bloqué: $STATUS"; exit 1; }
echo "✅ SSRF protection: OK"

# 5. Token revocation
TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login"   -H "Content-Type: application/json"   -d "{"email":"$TEST_EMAIL","password":"$TEST_PASSWORD"}" | jq -r .access_token)
curl -s -X POST "$BASE_URL/api/v1/auth/logout" -H "Authorization: Bearer $TOKEN" > /dev/null
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/auth/me"   -H "Authorization: Bearer $TOKEN")
[[ "$STATUS" == "401" ]] || { echo "❌ Token non révoqué après logout: $STATUS"; exit 1; }
echo "✅ Révocation de token: OK"

echo "=== ✅ TOUTES LES VÉRIFICATIONS PASSÉES ==="
