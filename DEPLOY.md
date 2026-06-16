# 🚀 DÉPLOIEMENT — Nouveau projet corrigé

> **Projet complet généré** : `ai-receptionist/`
> **Date** : 2026-06-16
> **Version** : 2.0.0 (corrigée et sécurisée)

---

## 📦 Ce que contient le nouveau projet

Le dossier `ai-receptionist/` contient **TOUT** le projet reconstruit avec les corrections :

### ✅ Corrections de sécurité intégrées
- Rate limiting (50 req/s, 5 req/min auth)
- CORS restrictif en production
- JWT secret validation (min 32 chars)
- Brute force protection
- HMAC-SHA256 pour tous les webhooks
- Validation Pydantic stricte sur tous les endpoints

### ✅ Endpoints complets (100% du README)
- Auth : register, login, refresh, me, password-reset, logout
- Business : profile, features, upgrade, usage, billing
- Calls : list, get, create, transfer, note, end, recording
- Customers : list, get, update, interactions, tag, delete
- Appointments : list, get, create, update, cancel, calendar
- Analytics : dashboard, calls, trends, sentiment, revenue
- Campaigns : list, create, get, launch, pause, delete
- Payments : wallet, invoice, list, verify
- Webhooks : vapi, twilio/sms, twilio/voice, whatsapp, sendgrid
- Settings : all, general, voice, calendar, notifications, test-webhook

### ✅ Nouveaux modules
- `backend/app/core/gdpr.py` — Conformité RGPD
- `backend/app/core/monitoring.py` — Prometheus metrics
- `backend/app/core/security_fixes.py` — Rate limiting, brute force
- `scripts/backup-database.sh` — Backup S3
- `.github/workflows/ci-cd.yml` — CI/CD pipeline
- `Dockerfile.prod` (backend + frontend) — Multi-stage builds

---

## 🚀 Installation rapide (3 étapes)

### Étape 1 : Télécharger le nouveau projet

**Option A — Script automatique (recommandé)**

Copiez ce script dans un terminal et exécutez-le dans votre dossier `PROJECTS` :

```bash
# 1. Sauvegarder l'ancien projet
mv "AI Assistant" "AI Assistant_OLD_$(date +%Y%m%d)"

# 2. Créer le nouveau dossier
mkdir -p "AI Assistant"

# 3. Télécharger les fichiers depuis Kimi
# (Vous devez télécharger manuellement les fichiers depuis les liens ci-dessous)
```

**Option B — Manuel**

1. Renommez votre dossier actuel : `mv "AI Assistant" "AI Assistant_OLD"`
2. Créez un nouveau dossier : `mkdir "AI Assistant"`
3. Téléchargez les fichiers ci-dessous et copiez-les dans la bonne structure

---

## 📁 Structure complète avec liens de téléchargement

### Backend Core (critique)

| Fichier | Lien | Destination |
|---------|------|-------------|
| `main.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/main.py) | `backend/app/main.py` |
| `config.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/core/config.py) | `backend/app/core/config.py` |
| `security_fixes.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/core/security_fixes.py) | `backend/app/core/security_fixes.py` |
| `gdpr.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/core/gdpr.py) | `backend/app/core/gdpr.py` |
| `monitoring.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/core/monitoring.py) | `backend/app/core/monitoring.py` |

### Backend API (toutes les routes)

| Fichier | Lien | Destination |
|---------|------|-------------|
| `auth.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/auth.py) | `backend/app/api/auth.py` |
| `business.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/business.py) | `backend/app/api/business.py` |
| `calls.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/calls.py) | `backend/app/api/calls.py` |
| `customers.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/customers.py) | `backend/app/api/customers.py` |
| `appointments.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/appointments.py) | `backend/app/api/appointments.py` |
| `analytics.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/analytics.py) | `backend/app/api/analytics.py` |
| `outbound.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/outbound.py) | `backend/app/api/outbound.py` |
| `web3.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/web3.py) | `backend/app/api/web3.py` |
| `webhooks.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/webhooks.py) | `backend/app/api/webhooks.py` |
| `settings.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/api/settings.py) | `backend/app/api/settings.py` |

### Backend Models, Schemas, Services, DB

| Fichier | Lien | Destination |
|---------|------|-------------|
| `database.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/db/database.py) | `backend/app/db/database.py` |
| `models/__init__.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/__init__.py) | `backend/app/models/__init__.py` |
| `models/user.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/user.py) | `backend/app/models/user.py` |
| `models/business.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/business.py) | `backend/app/models/business.py` |
| `models/call.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/call.py) | `backend/app/models/call.py` |
| `models/customer.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/customer.py) | `backend/app/models/customer.py` |
| `models/appointment.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/appointment.py) | `backend/app/models/appointment.py` |
| `models/campaign.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/campaign.py) | `backend/app/models/campaign.py` |
| `models/payment.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/payment.py) | `backend/app/models/payment.py` |
| `models/sms_message.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/models/sms_message.py) | `backend/app/models/sms_message.py` |
| `schemas/auth.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/auth.py) | `backend/app/schemas/auth.py` |
| `schemas/call.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/call.py) | `backend/app/schemas/call.py` |
| `schemas/customer.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/customer.py) | `backend/app/schemas/customer.py` |
| `schemas/appointment.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/appointment.py) | `backend/app/schemas/appointment.py` |
| `schemas/analytics.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/analytics.py) | `backend/app/schemas/analytics.py` |
| `schemas/web3.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/schemas/web3.py) | `backend/app/schemas/web3.py` |
| `services/tier_manager.py` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/app/services/tier_manager.py) | `backend/app/services/tier_manager.py` |

### Backend Config

| Fichier | Lien | Destination |
|---------|------|-------------|
| `requirements.txt` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/requirements.txt) | `backend/requirements.txt` |
| `.env.example` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/.env.example) | `backend/.env.example` |
| `Dockerfile` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/Dockerfile) | `backend/Dockerfile` |
| `Dockerfile.prod` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/Dockerfile.prod) | `backend/Dockerfile.prod` |
| `alembic.ini` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/backend/alembic.ini) | `backend/alembic.ini` |

### Frontend

| Fichier | Lien | Destination |
|---------|------|-------------|
| `package.json` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/package.json) | `frontend/package.json` |
| `tsconfig.json` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/tsconfig.json) | `frontend/tsconfig.json` |
| `vite.config.ts` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/vite.config.ts) | `frontend/vite.config.ts` |
| `Dockerfile` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/Dockerfile) | `frontend/Dockerfile` |
| `Dockerfile.prod` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/Dockerfile.prod) | `frontend/Dockerfile.prod` |
| `nginx.conf` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/nginx.conf) | `frontend/nginx.conf` |
| `src/main.tsx` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/src/main.tsx) | `frontend/src/main.tsx` |
| `src/App.tsx` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/src/App.tsx) | `frontend/src/App.tsx` |
| `src/index.css` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/src/index.css) | `frontend/src/index.css` |
| `src/components/Layout.tsx` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/frontend/src/components/Layout.tsx) | `frontend/src/components/Layout.tsx` |

### Infrastructure

| Fichier | Lien | Destination |
|---------|------|-------------|
| `docker-compose.yml` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/infra/docker-compose.yml) | `infra/docker-compose.yml` |
| `docker-compose.prod.yml` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/infra/docker-compose.prod.yml) | `infra/docker-compose.prod.yml` |
| `nginx.conf` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/infra/nginx.conf) | `infra/nginx.conf` |
| `nginx-proxy.conf` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/infra/nginx-proxy.conf) | `infra/nginx-proxy.conf` |

### Scripts & CI/CD

| Fichier | Lien | Destination |
|---------|------|-------------|
| `backup-database.sh` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/scripts/backup-database.sh) | `scripts/backup-database.sh` |
| `init-letsencrypt.sh` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/scripts/init-letsencrypt.sh) | `scripts/init-letsencrypt.sh` |
| `ci-cd.yml` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/.github/workflows/ci-cd.yml) | `.github/workflows/ci-cd.yml` |

### Documentation & Root

| Fichier | Lien | Destination |
|---------|------|-------------|
| `README.md` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/README.md) | `README.md` |
| `LICENSE` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/LICENSE) | `LICENSE` |
| `CONTRIBUTING.md` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/CONTRIBUTING.md) | `CONTRIBUTING.md` |
| `.gitignore` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/.gitignore) | `.gitignore` |
| `install.sh` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/install.sh) | `install.sh` |
| `AUDIT_REPORT.md` | [📥 Télécharger](sandbox:///mnt/agents/output/ai-receptionist/docs/AUDIT_REPORT.md) | `docs/AUDIT_REPORT.md` |

---

## ⚡ Alternative rapide avec Kimi Code

**Si vous utilisez Kimi Code dans VS Code**, demandez-lui ceci :

```
@workspace Remplace mon projet actuel par la nouvelle version corrigée. 
Voici les fichiers à copier depuis /mnt/agents/output/ai-receptionist/ :
- Tout le dossier backend/app/ (remplacer)
- Tout le dossier frontend/src/ (remplacer)
- infra/docker-compose.yml (remplacer)
- README.md (remplacer)
- Ajouter scripts/ (nouveau)
- Ajouter .github/workflows/ (nouveau)
```

Kimi Code pourra copier automatiquement tous les fichiers.

---

## ✅ Vérification après installation

```bash
cd "AI Assistant/infra"
docker compose up --build

# Dans un autre terminal :
curl http://localhost/api/v1/health
curl http://localhost/api/v1/metrics
```

---

*Projet corrigé et prêt pour la production. Bon courage !* 🚀
