#!/bin/bash
set -euo pipefail

echo "Checking critical secrets..."

if [[ ${#JWT_SECRET} -lt 32 ]]; then
  echo "JWT_SECRET too short (${#JWT_SECRET} chars, minimum 32)"
  exit 1
fi

DEFAULTS=("change-me-in-production" "changeme" "secret" "default" "")
for d in "${DEFAULTS[@]}"; do
  if [[ "$JWT_SECRET" == "$d" ]]; then
    echo "JWT_SECRET is a known default value!"
    exit 1
  fi
done

if [[ "${DEBUG:-false}" == "true" ]]; then
  echo "DEBUG=true in production!"
  exit 1
fi

if [[ -z "${PLATFORM_PRIVATE_KEY:-}" ]]; then
  echo "PLATFORM_PRIVATE_KEY empty — Web3 disabled"
fi

echo "Secrets validated"

echo "Testing Redis..."
redis-cli -u "$REDIS_URL" ping | grep -q "PONG" || { echo "Redis unreachable"; exit 1; }
echo "Redis OK"

echo "Testing PostgreSQL..."
pg_isready -d "$DATABASE_URL" || { echo "PostgreSQL unreachable"; exit 1; }
echo "PostgreSQL OK"
