#!/bin/bash
# =============================================================================
# Pre-deployment security check
# =============================================================================
set -euo pipefail

echo "🔍 Vérification des secrets critiques..."

if [[ ${#JWT_SECRET} -lt 32 ]]; then
  echo "❌ JWT_SECRET trop court (${#JWT_SECRET} chars, minimum 32)"
  exit 1
fi

DEFAULTS=("change-me-in-production" "changeme" "secret" "default" "")
for d in "${DEFAULTS[@]}"; do
  if [[ "$JWT_SECRET" == "$d" ]]; then
    echo "❌ JWT_SECRET est une valeur par défaut connue !"
    exit 1
  fi
done

if [[ "${DEBUG:-false}" == "true" ]]; then
  echo "❌ DEBUG=true en production !"
  exit 1
fi

if [[ -z "${PLATFORM_PRIVATE_KEY:-}" ]]; then
  echo "⚠️  PLATFORM_PRIVATE_KEY vide — Web3 désactivé"
fi

echo "✅ Secrets validés"

echo "🔍 Test Redis..."
redis-cli -u "$REDIS_URL" ping | grep -q "PONG" || { echo "❌ Redis inaccessible"; exit 1; }
echo "✅ Redis OK"

echo "🔍 Test PostgreSQL..."
pg_isready -d "$DATABASE_URL" || { echo "❌ PostgreSQL inaccessible"; exit 1; }
echo "✅ PostgreSQL OK"
