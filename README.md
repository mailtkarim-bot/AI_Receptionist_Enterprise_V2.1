# AI Receptionist Enterprise

<div align="center">

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**Multi-Channel AI Voice Agent with Web3 Payments — 3-Tier SaaS Platform**

[Overview](#overview) • [Features](#features) • [Pricing](#pricing) • [Architecture](#architecture) • [Quick Start](#quick-start) • [API Reference](#api-endpoints) • [Security](#security)

</div>

---

## ⚠️ Production Readiness Checklist

> **The following critical components are identified as missing or incomplete for a true production-grade deployment. These must be addressed before onboarding real enterprise clients.**

| # | Component | Severity | Status |
|---|-----------|----------|--------|
| 🟢 | **Security Middleware** | 🔴 CRITICAL | ✅ Implemented (rate limiting, CORS, JWT validation) |
| 🟢 | **Authentication** | 🔴 CRITICAL | ✅ Implemented (JWT + refresh + password reset) |
| 🟢 | **Webhook HMAC-SHA256** | 🔴 CRITICAL | ✅ Implemented (Vapi, Twilio, WhatsApp, SendGrid) |
| 🟢 | **GDPR Compliance** | 🔴 CRITICAL | ✅ Implemented (consent, purge, erasure, breach) |
| 🟢 | **Monitoring** | 🔴 CRITICAL | ✅ Implemented (Prometheus metrics, health check) |
| 🟢 | **Database Backup** | 🔴 CRITICAL | ✅ Implemented (S3 backup script) |
| 🟢 | **CI/CD Pipeline** | 🔴 CRITICAL | ✅ Provided (GitHub Actions template) |
| 🟢 | **Docker Production** | 🔴 CRITICAL | ✅ Provided (multi-stage Dockerfiles) |
| 🟡 | **Alembic Migrations** | 🟡 HIGH | ⚠️ Config file provided, migrations folder empty |
| 🟡 | **Tests** | 🟡 HIGH | ⚠️ Test folder structure ready, tests to be written |
| 🟡 | **Load Testing** | 🟡 HIGH | ❌ Not Implemented |
| 🟡 | **Penetration Testing** | 🟡 HIGH | ❌ Not Documented |
| 🟡 | **SLA & Uptime** | 🟡 HIGH | ❌ Not Documented |

---

## Overview

**AI Receptionist Enterprise** is a production-ready, multi-channel AI voice agent platform designed for businesses that need 24/7 intelligent call handling. Built with **FastAPI** and **React 19**, it integrates with **Vapi** (voice AI), **Twilio** (SMS), **WhatsApp**, **Google Calendar**, and **Web3 payments (USDC)** to deliver a complete receptionist-as-a-service solution.

The platform operates on a **3-tier SaaS model** (Basic / Professional / Enterprise) with feature gating, usage limits, and automated billing.

---

## Features

| # | Feature | Description | Min Tier |
|---|---------|-------------|----------|
| 📞 | **AI Voice Receptionist** | Handles inbound calls with natural conversation via Vapi AI | Basic |
| 💬 | **SMS Handling** | Two-way SMS conversations powered by Twilio | Basic |
| 💚 | **WhatsApp Integration** | Business WhatsApp messaging | Professional |
| 📧 | **Email Support** | Automated email responses via SendGrid | Enterprise |
| 📅 | **Smart Scheduling** | Google Calendar integration with conflict detection | Basic (1) / Pro (3) / Ent (10) |
| ⚠️ | **Emergency Detection** | AI-powered detection of emergency situations with escalation | Professional |
| 🧠 | **Customer Memory** | Persistent customer memory with vector embeddings for context | Professional |
| 📈 | **Sentiment Analytics** | Real-time sentiment analysis on all conversations | Professional |
| 📞 | **Outbound Campaigns** | Automated outbound call and SMS campaigns | Professional |
| 🛡️ | **Spam Filtering** | AI spam detection to block nuisance calls | Professional |
| 💰 | **Web3 USDC Payments** | Accept USDC on Ethereum/Base for invoices | Enterprise |
| 🎙️ | **Voice Cloning** | Custom brand voice with ElevenLabs | Enterprise |
| 🧾 | **NFT Receipts** | Blockchain-verified payment receipts | Enterprise |

---

## Pricing

### SaaS Tiers

| Feature | Basic $500/mo | Professional $800/mo | Enterprise $1,500/mo |
|---------|:-------------:|:--------------------:|:--------------------:|
| Voice + SMS | ✅ | ✅ | ✅ |
| WhatsApp | ❌ | ✅ | ✅ |
| Email | ❌ | ❌ | ✅ |
| Calendars | 1 | 3 | 10 |
| Emergency Detection | ❌ | ✅ | ✅ |
| Customer Memory | ❌ | ✅ | ✅ |
| Sentiment Analytics | ❌ | ✅ | ✅ |
| Outbound Campaigns | ❌ | ✅ | ✅ |
| Spam Filter | ❌ | ✅ | ✅ |
| Web3 USDC Payments | ❌ | ❌ | ✅ |
| Voice Cloning | ❌ | ❌ | ✅ |
| NFT Receipts | ❌ | ❌ | ✅ |
| Max Calls/Month | 500 | 2,000 | 10,000 |
| Support | Email | Email + Chat | Priority + Phone |

### Setup Fees

| Tier | Setup Fee | Monthly | Target Client |
|------|-----------|---------|---------------|
| **Basic** | $1,500 | $500/mo | Small service businesses |
| **Professional** | $2,500 | $800/mo | Clinics, agencies |
| **Enterprise** | $5,000 | $1,500/mo | Chains, corporates |

> **ROI Calculator**: A human receptionist costs ~$2,500/month and works 9-5. Our AI costs $500/month and works 24/7/365.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  React   │  │  Phone   │  │  WhatsApp│  │  Browser │  │  Mobile App  │  │
│  │   SPA    │  │  System  │  │  Client  │  │  WebRTC  │  │   (PWA)      │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       └─────────────┴──────────────┴──────────────┴────────────────┘          │
│                              Port 80 / 443                                   │
└────────────────────────────────────┼──────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼──────────────────────────────────────────┐
│                            NGINX PROXY                                       │
│  Reverse Proxy + Load Balancer + SSL Termination (Let's Encrypt)            │
└────────────────────────────────────┼──────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼──────────────────────────────────────────┐
│               API LAYER (FastAPI + Uvicorn)                                  │
│  REST API + WebSocket (Real-time) + Prometheus Metrics                     │
│  Auth / Business / Calls / Customers / Appointments / Analytics / Payments  │
└────────────────────────────────────┼──────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼──────────────────────────────────────────┐
│                      DATA & EXTERNAL SERVICES                                │
│  PostgreSQL 16 │ Redis 7 │ OpenAI GPT-4o │ Vapi │ Twilio │ SendGrid │ Web3  │
└───────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | React | 19 | UI framework |
| **Frontend** | TypeScript | 5.7 | Type safety |
| **Frontend** | Tailwind CSS | 4 | Utility-first styling |
| **Frontend** | Vite | 6 | Build tool |
| **Backend** | Python | 3.12 | Runtime |
| **Backend** | FastAPI | 0.115 | Web framework |
| **Backend** | Uvicorn | 0.34 | ASGI server |
| **Backend** | SQLAlchemy | 2.0 | ORM |
| **Backend** | Alembic | 1.14 | Migrations |
| **Backend** | Pydantic | 2.10 | Data validation |
| **Backend** | Celery | 5.4 | Background tasks |
| **Database** | PostgreSQL | 16 | Primary database |
| **Cache** | Redis | 7 | Caching & sessions |
| **AI/ML** | OpenAI GPT-4o | — | Conversational AI |
| **Voice** | Vapi | — | Voice AI platform |
| **SMS** | Twilio | — | SMS gateway |
| **Email** | SendGrid | — | Email delivery |
| **Payments** | Web3.py / USDC | — | Blockchain payments |
| **Proxy** | Nginx | Alpine | Reverse proxy |
| **SSL** | Let's Encrypt | — | Free SSL certificates |
| **Container** | Docker + Compose | — | Containerization |

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.20+
- [Git](https://git-scm.com/)

### 1. Clone & Configure

```bash
git clone https://github.com/your-org/ai-receptionist.git
cd ai-receptionist

# Copy environment file
cp backend/.env.example backend/.env

# Edit with your API keys
nano backend/.env
```

### 2. Start Services

```bash
cd infra
docker compose up -d
```

### 3. Run Migrations

```bash
docker compose exec api alembic upgrade head
```

### 4. Verify Health

```bash
curl http://localhost/api/v1/health
```

### 5. Access the App

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| API Docs | http://localhost/api/v1/docs (Swagger UI) |
| API (ReDoc) | http://localhost/api/v1/redoc |
| Metrics | http://localhost/api/v1/metrics |

---

## API Endpoints

### Authentication

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/api/v1/auth/register` | Register new business | No |
| `POST` | `/api/v1/auth/login` | Login & receive JWT tokens | No |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | Refresh Token |
| `GET` | `/api/v1/auth/me` | Get current business profile | JWT |
| `POST` | `/api/v1/auth/password-reset` | Request password reset | No |
| `POST` | `/api/v1/auth/password-reset/confirm` | Confirm password reset | Token |
| `POST` | `/api/v1/auth/logout` | Revoke current token | JWT |

### Business Management

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/business/` | Get business profile | JWT |
| `PUT` | `/api/v1/business/` | Update business profile | JWT |
| `GET` | `/api/v1/business/features` | Get enabled features | JWT |
| `POST` | `/api/v1/business/upgrade` | Upgrade subscription tier | JWT |
| `GET` | `/api/v1/business/usage` | Get usage statistics | JWT |
| `GET` | `/api/v1/business/billing` | Get billing history | JWT |

### Calls

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/calls` | List all calls | JWT |
| `GET` | `/api/v1/calls/{id}` | Get call details | JWT |
| `POST` | `/api/v1/calls` | Initiate outbound call | JWT |
| `POST` | `/api/v1/calls/{id}/transfer` | Transfer live call | JWT |
| `POST` | `/api/v1/calls/{id}/note` | Add call note | JWT |
| `POST` | `/api/v1/calls/{id}/end` | End active call | JWT |
| `GET` | `/api/v1/calls/{id}/recording` | Get recording URL | JWT |

### Customers

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/customers` | List customers | JWT |
| `GET` | `/api/v1/customers/{id}` | Get customer details | JWT |
| `PATCH` | `/api/v1/customers/{id}` | Update customer | JWT |
| `GET` | `/api/v1/customers/{id}/interactions` | Get customer history | JWT |
| `POST` | `/api/v1/customers/{id}/tag` | Tag customer | JWT |
| `DELETE` | `/api/v1/customers/{id}` | Delete customer | JWT |

### Appointments

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/appointments` | List appointments | JWT |
| `GET` | `/api/v1/appointments/{id}` | Get appointment details | JWT |
| `POST` | `/api/v1/appointments` | Create appointment | JWT |
| `PATCH` | `/api/v1/appointments/{id}` | Update appointment | JWT |
| `DELETE` | `/api/v1/appointments/{id}` | Cancel appointment | JWT |
| `GET` | `/api/v1/appointments/calendar` | Get calendar view | JWT |

### Analytics

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/analytics/dashboard` | Dashboard summary | JWT |
| `GET` | `/api/v1/analytics/calls` | Call analytics | JWT |
| `GET` | `/api/v1/analytics/trends` | Usage trends | JWT |
| `GET` | `/api/v1/analytics/sentiment` | Sentiment report | JWT |
| `GET` | `/api/v1/analytics/revenue` | Revenue analytics | JWT |

### Outbound Campaigns

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/campaigns` | List campaigns | JWT |
| `POST` | `/api/v1/campaigns` | Create campaign | JWT |
| `GET` | `/api/v1/campaigns/{id}` | Get campaign details | JWT |
| `POST` | `/api/v1/campaigns/{id}/launch` | Start campaign | JWT |
| `POST` | `/api/v1/campaigns/{id}/pause` | Pause campaign | JWT |
| `DELETE` | `/api/v1/campaigns/{id}` | Delete campaign | JWT |

### Web3 Payments (Enterprise Tier)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/payments/wallet` | Get payment wallet address | JWT |
| `POST` | `/api/v1/payments/invoice` | Create USDC invoice | JWT |
| `GET` | `/api/v1/payments/invoices` | List invoices | JWT |
| `POST` | `/api/v1/payments/verify` | Verify on-chain payment | JWT |

### Webhooks (External Services)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/api/v1/webhooks/vapi` | Vapi voice events | HMAC |
| `POST` | `/api/v1/webhooks/twilio/sms` | Twilio SMS inbound | HMAC |
| `POST` | `/api/v1/webhooks/twilio/voice` | Twilio voice events | HMAC |
| `POST` | `/api/v1/webhooks/whatsapp` | WhatsApp inbound messages | HMAC |
| `POST` | `/api/v1/webhooks/sendgrid` | SendGrid email events | HMAC |

### Settings

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/v1/settings` | Get all settings | JWT |
| `PATCH` | `/api/v1/settings/general` | Update general settings | JWT |
| `PATCH` | `/api/v1/settings/voice` | Update voice AI settings | JWT |
| `PATCH` | `/api/v1/settings/calendar` | Update calendar settings | JWT |
| `PATCH` | `/api/v1/settings/notifications` | Update notification settings | JWT |
| `POST` | `/api/v1/settings/test-webhook` | Test webhook connectivity | JWT |

---

## Security

### Authentication
- **JWT tokens** with HS256 algorithm and configurable expiry
- Access tokens (30 min) + Refresh tokens (7 days) rotation
- Password hashing with bcrypt (12 rounds)
- Brute force protection (5 attempts → 5min block, 10 attempts → 15min block)

### Data Protection
- **PII hashing** for sensitive customer data
- **AES-256 encryption** for conversation transcripts at rest
- Row-level security per business tenant

### Webhook Security
- **HMAC-SHA256 signature verification** for all incoming webhooks
- Replay attack protection with timestamp validation
- Timing-safe comparison (prevents timing attacks)

### API Security
- Rate limiting: 50 req/s per IP, 5 req/min on auth endpoints
- CORS configured per environment (restrictive in production)
- Input validation with Pydantic on all endpoints
- SQL injection prevention via SQLAlchemy ORM parameterized queries

### Infrastructure Security
- Docker containers run with `no-new-privileges`
- Read-only root filesystem for API containers
- Non-root user execution in containers
- Network segmentation with dedicated Docker bridge network
- Environment variables for all secrets (never hardcoded)

### Blockchain Security
- EIP-712 typed data signing for payment authorizations
- Nonce-based replay protection on all on-chain transactions
- Payment verification via direct RPC node query

---

## GDPR / RGPD Compliance

> **STATUS: IMPLEMENTED**

### Implemented Features

| # | Requirement | Status |
|---|-------------|--------|
| 1 | **Lawful Basis** | ✅ Explicit consent logging per caller |
| 2 | **Right to Erasure** | ✅ Automated deletion within 30 days of request |
| 3 | **Data Minimization** | ✅ Auto-purge after 90 days retention |
| 4 | **Privacy by Design** | ✅ Voice data encrypted at rest (AES-256) |
| 5 | **Consent Logging** | ✅ Immutable audit trail |
| 6 | **Breach Notification** | ✅ 72-hour notification workflow |

See `backend/app/core/gdpr.py` for implementation details.

---

## Monitoring & Observability

> **STATUS: IMPLEMENTED**

### Metrics Available

| Metric | Endpoint |
|--------|----------|
| HTTP requests total | `/api/v1/metrics` |
| Request latency histogram | `/api/v1/metrics` |
| Active calls gauge | `/api/v1/metrics` |
| Error rate counter | `/api/v1/metrics` |
| Health check | `/api/v1/health` |

### Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Metrics** | Prometheus | Request rate, latency, errors |
| **Health** | FastAPI endpoint | DB, Redis, API status |
| **Logs** | Structured JSON | Centralized logging |

---

## Automated Backup & Disaster Recovery

> **STATUS: PROVIDED**

### Backup Strategy

| Layer | Frequency | Retention | Tool |
|-------|-----------|-----------|------|
| **PostgreSQL Full** | Daily at 02:00 UTC | 30 days | pg_dump + S3 |
| **PostgreSQL WAL** | Continuous | 7 days | WAL archive |
| **Redis RDB** | Every 6 hours | 7 days | BGSAVE + S3 |

See `scripts/backup-database.sh` for implementation.

---

## Project Structure

```
ai-receptionist/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # Route handlers (all endpoints implemented)
│   │   ├── core/         # Config, security, logging, gdpr, monitoring
│   │   ├── db/           # Database engine, base, sessions
│   │   ├── integrations/ # External service integrations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas (strict validation)
│   │   ├── services/     # Business logic (tier management)
│   │   └── main.py       # Application entry (middleware stack)
│   ├── migrations/       # Alembic migrations (config ready)
│   ├── tests/            # Test suite (structure ready)
│   ├── Dockerfile        # Dev container
│   ├── Dockerfile.prod   # Production container (multi-stage)
│   ├── requirements.txt
│   └── .env.example      # Environment template
├── frontend/             # React 19 SPA
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Route pages
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API client
│   │   └── types/        # TypeScript types
│   ├── public/
│   ├── Dockerfile
│   ├── Dockerfile.prod   # Production (Vite → Nginx)
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── infra/                # Infrastructure
│   ├── docker-compose.yml      # Development stack
│   ├── docker-compose.prod.yml # Production stack
│   ├── nginx.conf              # Nginx reverse proxy
│   └── nginx-proxy.conf        # Proxy settings
├── scripts/              # Operational scripts
│   ├── backup-database.sh      # DB backup to S3
│   └── init-letsencrypt.sh   # SSL certificate init
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md   # System architecture
│   ├── API.md            # Complete API reference
│   ├── PRICING.md        # Pricing & ROI guide
│   └── AUDIT_REPORT.md   # Security audit report
├── .github/              # GitHub Actions
│   └── workflows/
│       └── ci-cd.yml     # Full CI/CD pipeline
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on code style, testing, and submission guidelines.

### Development Setup

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by the AI Receptionist Team**

[Website](https://aireceptionist.example.com) • [Docs](https://docs.aireceptionist.example.com) • [Support](mailto:support@aireceptionist.example.com)

</div>
