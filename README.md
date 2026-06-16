# AI Receptionist Enterprise V2 — Hardened

**Score de résilience : 78/100** | Statut : DÉPLOYABLE avec surveillance

## ⚠️ Changements majeurs (v2.1.0)

- **Sécurité** : PyJWT remplace python-jose, blacklist Redis cross-instance, brute force Redis
- **Webhooks** : Algorithmes corrects par fournisseur (Twilio HMAC-SHA1, Vapi HMAC-SHA256)
- **Web3** : Vérification on-chain réelle via Web3.py
- **GDPR** : `ConsentRecord` et `BreachLog` persistant en base
- **Database** : Alembic migrations, `SELECT FOR UPDATE` sur appointments
- **Rate limiting** : Redis sliding window, cluster-safe
- **SSRF** : Validation d'URL + httpx async
- **Metrics** : Protégées par `X-Metrics-Key`

## Quick Start (Production)

```bash
cd infra
docker network create nginx-proxy
mkdir -p secrets
echo "votre-jwt-secret-64-chars" > secrets/jwt_secret.txt
echo "votre-mdp-db" > secrets/db_password.txt
echo "votre-mdp-redis" > secrets/redis_password.txt
chmod 600 secrets/*

docker compose -f docker-compose.prod.yml up -d --build
cd ../backend
alembic upgrade head
```

## Vérification post-déploiement

```bash
./scripts/post-deploy-verify.sh
```

## Architecture

```
Client → Nginx (SSL, rate limit) → FastAPI (Redis rate limit, JWT) → PostgreSQL / Redis
```

## License

MIT
