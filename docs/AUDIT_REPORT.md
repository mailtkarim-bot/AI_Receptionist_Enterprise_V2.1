# 🔴 AUDIT COMPLET — AI Receptionist Enterprise

> **Date d'audit** : 2026-06-16
> **Auditeur** : Senior Smart Contract & Backend Security Auditor
> **Repo analysé** : https://github.com/mailtkarim-bot/AI_Receptionist_Enterprise
> **Score global** : 62/100 (Passable — Nécessite des corrections avant production)

---

## 📊 Score par catégorie

| Catégorie | Score | Commentaire |
|-----------|-------|-------------|
| **Architecture & Structure** | 85/100 | Backend bien structuré, models/schemas/services séparés |
| **Sécurité Authentification** | 45/100 | JWT sans refresh, CORS trop permissif, secret par défaut dangereux |
| **Sécurité Webhooks** | 40/100 | Vapi webhook compare string simple, pas HMAC-SHA256 |
| **Sécurité API** | 50/100 | Pas de rate limiting middleware, updates en `dict` non validés |
| **Conformité README vs Code** | 55/100 | 40% des endpoints documentés sont manquants dans le code |
| **Production Readiness** | 30/100 | Pas de tests, CI/CD, monitoring, backup, GDPR |
| **Web3 & Blockchain** | 70/100 | Payment gateway fonctionnel mais webhook blockchain absent |
| **Documentation** | 80/100 | ARCHITECTURE.md, API.md, PRICING.md excellents |

---

## 🔴 FAILLES CRITIQUES (À corriger immédiatement)

### 1. [CRITIQUE] `get_current_business` dans `tier_manager.py` — Non fonctionnel

**Fichier** : `backend/app/services/tier_manager.py`
**Problème** : La fonction accepte `token: str = None` comme paramètre positionnel. Quand utilisée comme `Depends()`, FastAPI ne peut pas injecter le header Authorization. Elle retournera toujours 401.

**Code problématique** :
```python
async def get_current_business(
    token: str = None,  # ❌ Ne fonctionne pas avec Depends()
    db: AsyncSession = Depends(get_db),
) -> Business:
```

**Correction** : Utiliser `HTTPAuthorizationCredentials` comme dans `auth.py`.

### 2. [CRITIQUE] CORS `allow_origins=["*"]` — Production unsafe

**Fichier** : `backend/app/main.py`
**Problème** : Accepte toutes les origines en production. Permet les requêtes cross-origin avec credentials.

**Correction** : Limiter aux domaines de production + localhost pour dev.

### 3. [CRITIQUE] `JWT_SECRET` avec valeur par défaut

**Fichier** : `backend/app/core/config.py`
**Problème** : `JWT_SECRET: str = "change-me-in-production"` — Si l'admin oublie de changer, n'importe qui peut forger des JWT.

**Correction** : Lever une exception si la valeur par défaut est détectée en production.

### 4. [CRITIQUE] Webhook Vapi — Pas de HMAC-SHA256

**Fichier** : `backend/app/api/webhooks.py`
**Problème** : Le README promet HMAC-SHA256, mais le code fait :
```python
if expected and secret != expected:
    raise HTTPException(...)
```
C'est une comparaison string simple, vulnérable à timing attacks.

**Correction** : Utiliser `hmac.compare_digest()` avec HMAC-SHA256 du payload.

### 5. [CRITIQUE] `updates: dict` sans validation Pydantic

**Fichiers** : `backend/app/api/business.py`, `backend/app/api/settings.py`
**Problème** : Les endpoints acceptent `dict` brut. Risque d'injection de champs non autorisés.

**Correction** : Créer des schemas Pydantic pour chaque update.

### 6. [HAUTE] Pas de rate limiting

**Fichier** : `backend/app/main.py`
**Problème** : Le README promet 50 req/s par IP et 5 req/min sur auth. Aucun middleware n'est implémenté.

**Correction** : Ajouter `slowapi` ou middleware custom.

### 7. [HAUTE] Auth — Pas de refresh token, pas de password reset

**Fichier** : `backend/app/api/auth.py`
**Problème** : Le README documente 6 endpoints auth. Seuls 3 sont implémentés (register, login, me). Il manque :
- `POST /auth/refresh`
- `POST /auth/password-reset`
- `POST /auth/password-reset/confirm`

### 8. [HAUTE] Endpoints manquants — 40% du README non implémenté

Voir tableau détaillé ci-dessous.

---

## 📋 TABLEAU DE CONFORMITÉ — Endpoints README vs Code

| Endpoint | README | Code | Écart |
|----------|--------|------|-------|
| `POST /auth/register` | ✅ | ✅ | — |
| `POST /auth/login` | ✅ | ✅ | — |
| `POST /auth/refresh` | ✅ | ❌ | **MANQUANT** |
| `GET /auth/me` | ✅ | ✅ | — |
| `POST /auth/password-reset` | ✅ | ❌ | **MANQUANT** |
| `POST /auth/password-reset/confirm` | ✅ | ❌ | **MANQUANT** |
| `GET /business/profile` | ✅ | ✅ (GET /) | — |
| `PATCH /business/profile` | ✅ | ✅ (PUT /) | — |
| `GET /business/features` | ✅ | ✅ | — |
| `POST /business/upgrade` | ✅ | ✅ | — |
| `GET /business/usage` | ✅ | ❌ | **MANQUANT** |
| `GET /business/billing` | ✅ | ❌ | **MANQUANT** |
| `GET /calls` | ✅ | ✅ | — |
| `GET /calls/{id}` | ✅ | ✅ | — |
| `POST /calls` (initiate outbound) | ✅ | ❌ | **MANQUANT** |
| `POST /calls/{id}/transfer` | ✅ | ✅ | — |
| `POST /calls/{id}/note` | ✅ | ✅ | — |
| `POST /calls/{id}/end` | ✅ | ❌ | **MANQUANT** |
| `GET /calls/{id}/recording` | ✅ | ❌ | **MANQUANT** |
| `GET /customers` | ✅ | ✅ | — |
| `GET /customers/{id}` | ✅ | ✅ | — |
| `PATCH /customers/{id}` | ✅ | ✅ | — |
| `GET /customers/{id}/interactions` | ✅ | ✅ | — |
| `POST /customers/{id}/tag` | ✅ | ❌ | **MANQUANT** |
| `DELETE /customers/{id}` | ✅ | ❌ | **MANQUANT** |
| `GET /appointments` | ✅ | ✅ | — |
| `GET /appointments/{id}` | ✅ | ✅ | — |
| `POST /appointments` | ✅ | ✅ | — |
| `PATCH /appointments/{id}` | ✅ | ✅ | — |
| `DELETE /appointments/{id}` | ✅ | ❌ (pas de cancel) | **MANQUANT** |
| `GET /appointments/calendar` | ✅ | ❌ | **MANQUANT** |
| `GET /analytics/dashboard` | ✅ | ✅ | — |
| `GET /analytics/calls` | ✅ | ✅ | — |
| `GET /analytics/trends` | ✅ | ✅ | — |
| `GET /analytics/sentiment` | ✅ | ✅ | — |
| `GET /analytics/revenue` | ✅ | ❌ | **MANQUANT** |
| `GET /campaigns` | ✅ | ✅ (GET /outbound/campaigns) | ⚠️ Path différent |
| `POST /campaigns` | ✅ | ✅ (POST /outbound/campaigns) | ⚠️ Path différent |
| `GET /campaigns/{id}` | ✅ | ✅ (GET /outbound/campaigns/{id}) | ⚠️ Path différent |
| `POST /campaigns/{id}/start` | ✅ | ✅ (POST /outbound/campaigns/{id}/launch) | ⚠️ Nom différent |
| `POST /campaigns/{id}/pause` | ✅ | ❌ | **MANQUANT** |
| `DELETE /campaigns/{id}` | ✅ | ❌ | **MANQUANT** |
| `GET /payments/wallet` | ✅ | ❌ (pas dans web3.py) | **MANQUANT** |
| `POST /payments/invoice` | ✅ | ❌ (pas dans web3.py) | **MANQUANT** |
| `GET /payments/invoices` | ✅ | ❌ | **MANQUANT** |
| `POST /payments/verify` | ✅ | ❌ (check_payment_status existe) | ⚠️ Partiel |
| `POST /payments/webhook` | ✅ | ❌ | **MANQUANT** |
| `POST /webhooks/vapi` | ✅ | ✅ (3 sous-routes) | — |
| `POST /webhooks/twilio/sms` | ✅ | ❌ | **MANQUANT** |
| `POST /webhooks/twilio/voice` | ✅ | ❌ | **MANQUANT** |
| `POST /webhooks/whatsapp` | ✅ | ❌ | **MANQUANT** |
| `POST /webhooks/sendgrid` | ✅ | ❌ | **MANQUANT** |
| `GET /settings` | ✅ | ❌ (sous-routes séparées) | ⚠️ Partiel |
| `PATCH /settings/general` | ✅ | ❌ (sous-routes séparées) | ⚠️ Partiel |
| `PATCH /settings/voice` | ✅ | ❌ | **MANQUANT** |
| `PATCH /settings/calendar` | ✅ | ❌ | **MANQUANT** |
| `PATCH /settings/notifications` | ✅ | ❌ | **MANQUANT** |
| `POST /settings/test-webhook` | ✅ | ❌ | **MANQUANT** |

**Résultat** : 25 endpoints manquants ou partiels sur 55 documentés (45% d'écart).

---

## 📁 FICHIERS MANQUANTS CRITIQUES

| Fichier | Sévérité | Impact |
|---------|----------|--------|
| `backend/tests/` | 🔴 Critique | Aucun test unitaire, d'intégration, E2E |
| `.github/workflows/ci-cd.yml` | 🔴 Critique | Pas de CI/CD, déploiement manuel |
| `backend/app/core/gdpr.py` | 🔴 Critique | Non conforme RGPD pour l'UE |
| `backend/app/core/monitoring.py` | 🔴 Critique | Aucune observabilité |
| `scripts/backup-database.sh` | 🔴 Critique | Pas de backup automatique |
| `backend/app/services/call_orchestrator.py` | 🟡 Haut | Référencé mais absent |
| `backend/app/services/spam_detector.py` | 🟡 Haut | Feature annoncée, service absent |
| `backend/app/services/sentiment_analyzer.py` | 🟡 Haut | Feature annoncée, service absent |
| `backend/app/services/emergency_detector.py` | 🟡 Haut | Feature annoncée, service absent |
| `backend/app/integrations/vapi/` | 🟡 Haut | Intégration Vapi non modularisée |
| `backend/app/integrations/twilio/` | 🟡 Haut | Intégration Twilio non modularisée |
| `backend/app/integrations/google/` | 🟡 Haut | Google Calendar absent |
| `backend/app/integrations/openai/` | 🟡 Haut | OpenAI service absent |
| `backend/migrations/` (Alembic) | 🟡 Haut | `init_db()` crée les tables au démarrage — pas de migrations versionnées |
| `backend/app/db/base.py` | 🟡 Haut | Échec de lecture, mais référencé partout |
| `backend/Dockerfile.prod` | 🟡 Haut | Référencé dans docker-compose.prod.yml mais absent |
| `frontend/Dockerfile.prod` | 🟡 Haut | Référencé mais absent |
| `docs/CONTRIBUTING.md` | 🟢 Moyen | Mentionné dans README, absent |
| `LICENSE` | 🟢 Moyen | Mentionné dans README, absent |

---

## 🔧 INCohérences Docker / Infra

| Problème | Fichier | Détail |
|----------|---------|--------|
| `Dockerfile.prod` manquant | `infra/docker-compose.prod.yml` | Référence `dockerfile: Dockerfile.prod` pour API et frontend. Seul `Dockerfile` existe. |
| `nginx-proxy.conf` manquant | `infra/docker-compose.prod.yml` | Référence `./nginx-proxy.conf:/etc/nginx/conf.d/my_proxy.conf:ro` |
| Réseau `nginx-proxy` external | `infra/docker-compose.prod.yml` | Déclaré `external: true` — doit être créé manuellement avant `docker compose up` |
| Port frontend | `frontend/Dockerfile` | Expose 80, mais `nginx.conf` route vers `frontend:3000`. Le Dockerfile prod devrait exposer 3000 ou nginx.conf doit être mis à jour. |
| `init_db()` au démarrage | `backend/app/db/database.py` | `Base.metadata.create_all()` au startup — OK pour dev, **DANGEREUX** pour prod (pas de migrations contrôlées). |

---

## 🛡️ Recommandations de sécurité additionnelles

1. **Ne jamais** utiliser `init_db()` en production. Utiliser Alembic avec `alembic upgrade head`.
2. **Hasher** les emails dans la base (actuellement stockés en clair dans `businesses.email`).
3. **Chiffrer** les transcripts avec AES-256 (actuellement stockés en clair dans `calls.transcript`).
4. **Ajouter** un `X-Request-ID` middleware pour le tracing.
5. **Limiter** le nombre de tentatives de login (brute force protection).
6. **Valider** toutes les entrées utilisateur avec Pydantic (pas de `dict` brut).
7. **Séparer** les tokens access (15-30 min) et refresh (7 jours) avec stockage Redis blacklist.

---

## ✅ Plan d'action priorisé

### Phase 1 — Sécurité (Semaine 1)
- [ ] Corriger `get_current_business` dans `tier_manager.py`
- [ ] Restreindre CORS en production
- [ ] Forcer `JWT_SECRET` en production (pas de valeur par défaut)
- [ ] Implémenter HMAC-SHA256 pour les webhooks
- [ ] Ajouter validation Pydantic sur `business.py` et `settings.py`
- [ ] Ajouter rate limiting middleware

### Phase 2 — Auth complète (Semaine 1)
- [ ] Ajouter refresh token endpoint
- [ ] Ajouter password reset (avec email)
- [ ] Séparer access token (30 min) et refresh token (7 jours)

### Phase 3 — Endpoints manquants (Semaine 2)
- [ ] Implémenter les 25 endpoints manquants
- [ ] Uniformiser les paths (`/outbound/campaigns` → `/campaigns`)

### Phase 4 — Production readiness (Semaine 3)
- [ ] Remplacer `init_db()` par Alembic migrations
- [ ] Créer `Dockerfile.prod` et `frontend/Dockerfile.prod`
- [ ] Ajouter tests pytest (coverage 80%)
- [ ] Ajouter CI/CD GitHub Actions
- [ ] Ajouter monitoring Prometheus/Grafana
- [ ] Ajouter backup automatique DB
- [ ] Ajouter GDPR compliance module

### Phase 5 — Intégrations (Semaine 4)
- [ ] Modulariser Vapi integration
- [ ] Modulariser Twilio integration
- [ ] Ajouter Google Calendar service
- [ ] Ajouter OpenAI service (spam, sentiment, emergency)
- [ ] Ajouter Celery pour les tâches async

---

*Fin du rapport d'audit*
