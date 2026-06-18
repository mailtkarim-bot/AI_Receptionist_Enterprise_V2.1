<div align="center">  
   
# 🤖 AI Receptionist Enterprise  
   
**Full-Stack SaaS Architecture Demo — v2.1**  
   
[![Version](https://img.shields.io/badge/version-2.1.0--demo-blue?style=for-the-badge)](https://github.com/mailtkarim-bot/AI_Receptionist_Enterprise_V2.1)  
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)  
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://postgresql.org)  
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io)  
[![Docker](https://img.shields.io/badge/Docker-24-2496ED?logo=docker)](https://docker.com)  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Security](https://img.shields.io/badge/Security-Self--Reviewed%20v2.1-orange?style=flat&logo=shield)](SECURITY.md)  
[![Pro Toolkit](https://img.shields.io/badge/Freelance%20Toolkit-Click%20Here-green?style=flat&logo=tool)](https://github.com/mailtkarim-bot/AI_Receptionist_Pro)  
   
**AI Voice · SMS · WhatsApp · Email · Google Calendar · Web3 USDC · JWT + Redis · Docker**  
   
[📐 Architecture](#-architecture) · [🚀 Quick Start](#-quick-start) · [💰 Business Model Research](#-business-model-research) · [🔐 Security](#-security) · [📞 Contact](#-contact)  
   
</div>  
   
---  
   
## Overview  
   
**AI Receptionist Enterprise** is a **full-stack architecture demonstration** for a multi-channel AI voice agent platform. Built with **FastAPI** and **React 19**, it integrates with **Vapi** (voice AI), **Twilio** (SMS), **WhatsApp**, **Google Calendar**, and **Web3 payments (USDC)** to showcase a complete receptionist-as-a-service architecture.  
   
The platform is designed around a **3-tier SaaS model** (Basic / Professional / Enterprise) with feature gating, usage limits, and billing logic — demonstrating product strategy and technical architecture skills.  
   
**v2.1 Némésis Review**: Self-directed security audit identifying 20+ issues, with 12 fully corrected and 8 documented as pending or requiring third-party integration.  
   
---  
   
## Implementation Status  
   
| Feature | Status | Notes |  
|---------|--------|-------|  
| AI Voice Webhook (Vapi) | ✅ Functional | HMAC-SHA256 verified, call logging, appointment extraction |  
| SMS Handling (Twilio) | ✅ Functional | Two-way SMS, E.164 validation, confirmation messages |  
| Google Calendar Sync | ✅ Functional | OAuth 2.0, event creation, conflict detection |  
| JWT Authentication | ✅ Functional | Access + refresh tokens, Redis blacklist, brute force protection |  
| Tier Management | ✅ Functional | Feature gating, usage limits, subscription logic |  
| Customer Management | ✅ Functional | CRUD, tagging, interaction history |  
| Call Logging & Analytics | ✅ Functional | Dashboard metrics, sentiment analysis stubs |  
| WhatsApp Integration | ⚠️ Stub | Webhook endpoint ready, deep integration pending |  
| Email (SendGrid) | ⚠️ Stub | SMTP config ready, campaign logic pending |  
| Web3 USDC Payments | ⚠️ Stub | Wallet generation, invoice creation, on-chain verification requires RPC node |  
| Voice Cloning | ❌ Not Implemented | ElevenLabs integration planned |  
| NFT Receipts | ❌ Not Implemented | ERC-721 contract design planned |  
   
---  
   
## Features  
   
| # | Feature | Description | Min Tier | Status |  
|---|---------|-------------|----------|--------|  
| 📞 | **AI Voice Receptionist** | Handles inbound calls with natural conversation via Vapi AI | Basic | ✅ |  
| 💬 | **SMS Handling** | Two-way SMS conversations powered by Twilio | Basic | ✅ |  
| 💚 | **WhatsApp Integration** | Business WhatsApp messaging (Pro+ tier) | Professional | ⚠️ Stub |  
| 📧 | **Email Support** | Automated email responses via SendGrid (Enterprise tier) | Enterprise | ⚠️ Stub |  
| 📆 | **Smart Scheduling** | Google Calendar integration with conflict detection | Basic (1) / Pro (3) / Ent (10) | ✅ |  
| ⚠️ | **Emergency Detection** | AI-powered detection of emergency situations with escalation | Professional | ✅ |  
| 🧠 | **Customer Memory** | Persistent customer memory with vector embeddings for context | Professional | ⚠️ Partial |  
| 📈 | **Sentiment Analytics** | Real-time sentiment analysis on all conversations | Professional | ⚠️ Partial |  
| 📞 | **Outbound Campaigns** | Automated outbound call and SMS campaigns | Professional | ⚠️ Stub |  
| 🛡️ | **Spam Filtering** | AI spam detection to block nuisance calls | Professional | ⚠️ Stub |  
| 💰 | **Web3 USDC Payments** | Accept USDC on Ethereum/Base for invoices (Enterprise) | Enterprise | ⚠️ Stub |  
| 🎤 | **Voice Cloning** | Custom brand voice with ElevenLabs (Enterprise) | Enterprise | ❌ |  
| 🧾 | **NFT Receipts** | Blockchain-verified payment receipts (Enterprise) | Enterprise | ❌ |  
   
---  
   
## Business Model Research  
   
> **Note:** These figures are based on **competitive market research** (Vapi.ai pricing, Twilio rates, Render hosting costs, Dubai clinic salary benchmarks). This project is **not commercially sold**. It serves as a **portfolio demonstration of pricing strategy design** and SaaS business modeling.  
   
### Hypothetical SaaS Tiers  
   
| Feature | Basic $500/mo | Professional $800/mo | Enterprise $1,500/mo |  
|---------|---------------|----------------------|----------------------|  
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
   
### Hypothetical Setup Fees  
   
| Tier | Setup Fee | Monthly | Target Client |  
|------|-----------|---------|---------------|  
| **Basic** | $1,500 | $500/mo | Small service businesses (plumbers, electricians, solo practices) |  
| **Professional** | $2,500 | $800/mo | Clinics, agencies, multi-staff businesses |  
| **Enterprise** | $5,000 | $1,500/mo | Chains, corporates, franchises |  
   
> **ROI Analysis:** A human receptionist costs ~$2,500/month and works 9-5. An AI receptionist at $500/month works 24/7/365. This demonstrates **business case modeling** skills, not an active commercial offer.  
   
---  
   
## Architecture  
   
```  
┌─────────────────────────────────────────────────────────────────────────────┐  
│                              CLIENT LAYER                                    │  
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  
│  │  React   │  │  Phone   │  │  WhatsApp│  │  Browser │  │  Mobile App  │  │  
│  │   SPA    │  │  System  │  │  Client  │  │  WebRTC  │  │   (PWA)      │  │  
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │  
│       │             │              │              │                │          │  
│       └─────────────┴──────────────┴──────────────┴────────────────┘          │  
│                                    │                                          │  
│                              Port 80 / 443                                   │  
└────────────────────────────────────┼──────────────────────────────────────────┘  
                                     │  
┌────────────────────────────────────┼──────────────────────────────────────────┐  
│                            NGINX PROXY                                       │  
│  ┌─────────────────────────────────┼───────────────────────────────────────┐  │  
│  │  Reverse Proxy + Load Balancer  │  SSL Termination (Let's Encrypt)    │  │  
│  │  Rate Limiting / Gzip / CORS    │  Static Asset Cache                 │  │  
│  └────────────────┬────────────────┴────────────────┬──────────────────────┘  │  
│                   │                                 │                          │  
│              /api/*                            /ws/* (WebSocket)               │  
│                   │                                 │                          │  
└───────────────────┼─────────────────────────────────┼──────────────────────────┘  
                    │                                 │  
┌───────────────────┼─────────────────────────────────┼──────────────────────────┐  
│               API LAYER (FastAPI + Uvicorn)                                  │  
│                                                                               │  
│  ┌──────────────────────────┐    ┌─────────────────────────────────────────┐  │  
│  │     REST API (HTTP)      │    │       WebSocket (Real-time)             │  │  
│  │  Auth / Business / Calls │    │  Live Call Status / Dashboard Stream    │  │  
│  │  Customers / Analytics   │    │  Agent Notifications                    │  │  
│  └────────────┬─────────────┘    └─────────────────────────────────────────┘  │  
│               │                                                               │  
│  ┌────────────┴───────────────────────────────────────────────────────────┐   │  
│  │                        Service Layer                                  │   │  
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │   │  
│  │  │  Auth    │ │ Business │ │  Call    │ │ Customer │ │  Booking  │  │   │  
│  │  │ Service  │ │ Service  │ │ Service  │ │ Service  │ │  Service  │  │   │  
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────────┘  │   │  
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │   │  
│  │  │ Campaign │ │ Payment  │ │  Spam    │ │Sentiment │ │ Emergency │  │   │  
│  │  │ Service  │ │ Service  │ │ Service  │ │ Service  │ │ Service   │  │   │  
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────────┘  │   │  
│  └────────────────────────┬──────────────────────────────────────────────┘   │  
└───────────────────────────┼──────────────────────────────────────────────────┘  
                            │  
┌───────────────────────────┼──────────────────────────────────────────────────┐  
│                      DATA & EXTERNAL SERVICES                                │  
│                                                                               │  
│  ┌──────────────┐  ┌───────────┐  ┌──────────┐  ┌─────────────────────┐   │  
│  │  PostgreSQL  │  │   Redis   │  │  OpenAI  │  │  Vapi (Voice AI)    │   │  
│  │    16-Alpine │  │  7-Alpine │  │   GPT-4o │  │  Twilio (SMS)       │   │  
│  │              │  │           │  │Embeddings│  │  SendGrid (Email)   │   │  
│  └──────────────┘  └───────────┘  └──────────┘  └─────────────────────┘   │  
│                                                                               │  
│  ┌─────────────────────────────────────────────────────────────────────┐    │  
│  │                      Web3 / Blockchain                              │    │  
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │    │  
│  │  │ USDC (ERC-20)│  │NFT Receipts  │  │Wallet Connect / MetaMask │ │    │  
│  │  │ Infura/Alchemy│  │ (ERC-721)    │  │EIP-712 Signatures       │ │    │  
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘ │    │  
│  └─────────────────────────────────────────────────────────────────────┘    │  
│                                                                               │  
│  ┌─────────────────────────────────────────────────────────────────────┐    │  
│  │                      External APIs                                  │    │  
│  │  Google Calendar API │ WhatsApp Business API │ ElevenLabs Voice   │    │  
│  └─────────────────────────────────────────────────────────────────────┘    │  
└───────────────────────────────────────────────────────────────────────────────┘  
```  
   
### Technology Stack  
   
| Layer | Technology | Version | Purpose |  
|-------|------------|---------|---------|  
| **Frontend** | React | 19 | UI framework |  
| **Frontend** | TypeScript | 5.7 | Type safety |  
| **Frontend** | Tailwind CSS | 4 | Utility-first styling |  
| **Frontend** | Vite | 6 | Build tool & dev server |  
| **Backend** | Python | 3.12 | Runtime |  
| **Backend** | FastAPI | 0.115 | Web framework |  
| **Backend** | Uvicorn | 0.34 | ASGI server |  
| **Backend** | SQLAlchemy | 2.0 | ORM |  
| **Backend** | Alembic | 1.14 | Database migrations |  
| **Backend** | Pydantic | 2.10 | Data validation |  
| **Backend** | Celery | 5.4 | Background tasks |  
| **Database** | PostgreSQL | 16 | Primary database |  
| **Cache** | Redis | 7 | Caching & sessions |  
| **AI/ML** | OpenAI GPT-4o | — | Conversational AI |  
| **AI/ML** | text-embedding-3-small | — | Vector embeddings |  
| **Voice** | Vapi | — | Voice AI platform |  
| **SMS** | Twilio | — | SMS gateway |  
| **Email** | SendGrid | — | Email delivery |  
| **Payments** | Web3.py / USDC | — | Blockchain payments (stub) |  
| **Proxy** | Nginx | Alpine | Reverse proxy |  
| **SSL** | Let's Encrypt | — | Free SSL certificates |  
| **Container** | Docker + Compose | — | Containerization |  
   
---  
   
## Quick Start  
   
### Prerequisites  
   
- Docker 24+  
- Docker Compose 2.20+  
- Git  
   
### 1. Clone & Configure  
   
```  
git clone https://github.com/mailtkarim-bot/AI_Receptionist_Enterprise_V2.git  
cd AI_Receptionist_Enterprise_V2  
   
# Copy environment file  
cp backend/.env.example backend/.env  
   
# Edit with your API keys  
nano backend/.env  
```  
   
### 2. Start Services  
   
```  
cd infra  
docker compose up -d  
```  
   
### 3. Run Migrations  
   
```  
docker compose exec api alembic upgrade head  
```  
   
### 4. Verify Health  
   
```  
# API healthcheck  
curl http://localhost/api/v1/health  
   
# All services  
docker compose ps  
```  
   
### 5. Access the App  
   
| Service | URL |  
|---------|-----|  
| Frontend | http://localhost |  
| API Docs | http://localhost/api/v1/docs (Swagger UI) |  
| API (ReDoc) | http://localhost/api/v1/redoc |  
   
### Development Mode  
   
```  
# Watch logs  
docker compose logs -f api  
   
# Restart a service  
docker compose restart api  
   
# Stop everything  
docker compose down  
   
# Stop and remove volumes  
docker compose down -v  
```  
   
---  
   
## API Endpoints  
   
> **Note:** 55 endpoints are **defined and documented**. ~30 are fully implemented with business logic. ~15 are stubs returning `501 Not Implemented` or mock data. ~10 require third-party integration (SendGrid, ElevenLabs) to be functional.  
   
### Authentication  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `POST` | `/api/v1/auth/register` | Register new business | No | ✅ |  
| `POST` | `/api/v1/auth/login` | Login & receive JWT tokens | No | ✅ |  
| `POST` | `/api/v1/auth/refresh` | Refresh access token | Refresh Token | ✅ |  
| `GET` | `/api/v1/auth/me` | Get current business profile | JWT | ✅ |  
| `POST` | `/api/v1/auth/password-reset` | Request password reset | No | ✅ |  
| `POST` | `/api/v1/auth/password-reset/confirm` | Confirm password reset | Token | ✅ |  
| `POST` | `/api/v1/auth/logout` | Revoke current token (Redis) | JWT | ✅ |  
   
### Business Management  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/business/profile` | Get business profile | JWT | ✅ |  
| `PATCH` | `/api/v1/business/profile` | Update business profile | JWT | ✅ |  
| `GET` | `/api/v1/business/features` | Get enabled features | JWT | ✅ |  
| `POST` | `/api/v1/business/upgrade` | Upgrade subscription tier | JWT | ⚠️ Stub (returns 501) |  
| `GET` | `/api/v1/business/usage` | Get usage statistics | JWT | ✅ |  
| `GET` | `/api/v1/business/billing` | Get billing history | JWT | ⚠️ Stub |  
   
### Calls  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/calls` | List all calls | JWT | ✅ |  
| `GET` | `/api/v1/calls/{id}` | Get call details | JWT | ✅ |  
| `POST` | `/api/v1/calls` | Initiate outbound call | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/calls/{id}/transfer` | Transfer live call | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/calls/{id}/note` | Add call note | JWT | ✅ |  
| `POST` | `/api/v1/calls/{id}/end` | End active call | JWT | ✅ |  
| `GET` | `/api/v1/calls/{id}/recording` | Get call recording URL | JWT | ⚠️ Stub |  
   
### Customers  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/customers` | List customers | JWT | ✅ |  
| `GET` | `/api/v1/customers/{id}` | Get customer details | JWT | ✅ |  
| `PATCH` | `/api/v1/customers/{id}` | Update customer | JWT | ✅ |  
| `GET` | `/api/v1/customers/{id}/interactions` | Get customer history | JWT | ✅ |  
| `POST` | `/api/v1/customers/{id}/tag` | Tag customer | JWT | ✅ |  
| `DELETE` | `/api/v1/customers/{id}` | Delete customer | JWT | ✅ |  
   
### Appointments  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/appointments` | List appointments | JWT | ✅ |  
| `GET` | `/api/v1/appointments/{id}` | Get appointment details | JWT | ✅ |  
| `POST` | `/api/v1/appointments` | Create appointment | JWT | ✅ |  
| `PATCH` | `/api/v1/appointments/{id}` | Update appointment | JWT | ✅ |  
| `DELETE` | `/api/v1/appointments/{id}` | Cancel appointment | JWT | ✅ |  
| `GET` | `/api/v1/appointments/calendar` | Get calendar view | JWT | ✅ |  
   
### Analytics  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/analytics/dashboard` | Dashboard summary | JWT | ✅ |  
| `GET` | `/api/v1/analytics/calls` | Call analytics | JWT | ✅ |  
| `GET` | `/api/v1/analytics/trends` | Usage trends | JWT | ⚠️ Stub |  
| `GET` | `/api/v1/analytics/sentiment` | Sentiment report | JWT | ⚠️ Stub |  
| `GET` | `/api/v1/analytics/revenue` | Revenue analytics | JWT | ⚠️ Stub |  
   
### Outbound Campaigns  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/campaigns` | List campaigns | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/campaigns` | Create campaign | JWT | ⚠️ Stub |  
| `GET` | `/api/v1/campaigns/{id}` | Get campaign details | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/campaigns/{id}/start` | Start campaign | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/campaigns/{id}/pause` | Pause campaign | JWT | ⚠️ Stub |  
| `DELETE` | `/api/v1/campaigns/{id}` | Delete campaign | JWT | ⚠️ Stub |  
   
### Web3 Payments (Enterprise Tier)  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/payments/wallet` | Get payment wallet address | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/payments/invoice` | Create USDC invoice | JWT | ⚠️ Stub |  
| `GET` | `/api/v1/payments/invoices` | List invoices | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/payments/verify` | Verify on-chain payment | JWT | ⚠️ Stub |  
| `POST` | `/api/v1/payments/webhook` | Blockchain webhook (automated) | HMAC | ⚠️ Stub |  
   
### Webhooks (External Services)  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `POST` | `/api/v1/webhooks/vapi` | Vapi voice events | HMAC-SHA256 | ✅ |  
| `POST` | `/api/v1/webhooks/twilio/sms` | Twilio SMS inbound | HMAC-SHA1 | ✅ |  
| `POST` | `/api/v1/webhooks/twilio/voice` | Twilio voice events | HMAC-SHA1 | ✅ |  
| `POST` | `/api/v1/webhooks/whatsapp` | WhatsApp inbound messages | HMAC-SHA256 | ⚠️ Stub |  
| `POST` | `/api/v1/webhooks/sendgrid` | SendGrid email events | HMAC-SHA256 | ⚠️ Stub |  
   
### Settings  
   
| Method | Path | Description | Auth | Status |  
|--------|------|-------------|------|--------|  
| `GET` | `/api/v1/settings` | Get all settings | JWT | ✅ |  
| `PATCH` | `/api/v1/settings/general` | Update general settings | JWT | ✅ |  
| `PATCH` | `/api/v1/settings/voice` | Update voice AI settings | JWT | ✅ |  
| `PATCH` | `/api/v1/settings/calendar` | Update calendar settings | JWT | ✅ |  
| `PATCH` | `/api/v1/settings/notifications` | Update notification settings | JWT | ✅ |  
| `POST` | `/api/v1/settings/test-webhook` | Test webhook connectivity | JWT | ✅ |  
   
---  
   
## Security  
   
### Authentication  
   
- **JWT tokens** with HS256 algorithm and configurable expiry  
- Access tokens (30 min) + Refresh tokens (7 days) rotation  
- **Redis-backed token blacklist** — cross-instance, cross-worker revocation  
- Password hashing with bcrypt (12 rounds)  
- **Brute force protection** — Redis sliding window, 5 attempts → 5min block  
   
### Data Protection  
   
- **PII hashing** for sensitive customer data (phone numbers, emails)  
- **AES-256 encryption** for conversation transcripts at rest (planned)  
- Row-level security per business tenant (planned)  
- **`is_active` flag** on Business model for account suspension  
   
### Webhook Security  
   
- **Vapi** : HMAC-SHA256 signature verification + timestamp anti-replay  
- **Twilio** : HMAC-SHA1 per official spec (URL + sorted params)  
- **WhatsApp** : HMAC-SHA256 with APP_SECRET only (no fallback)  
- **SendGrid** : HMAC-SHA256 with WEBHOOK_SECRET only (no fallback)  
- Replay attack protection with timestamp validation  
   
### API Security  
   
- **Rate limiting**: Redis sliding window, 50 req/s per IP, 5 req/min on auth  
- CORS configured per environment (restrictive in production)  
- Input validation with Pydantic on all endpoints  
- SQL injection prevention via SQLAlchemy ORM parameterized queries  
- **SSRF protection** on webhook test endpoint (URL validation + blocked hosts)  
   
### Infrastructure Security  
   
- Docker containers run with `no-new-privileges`  
- Read-only root filesystem for API containers (planned)  
- Resource limits (CPU/memory) on all services  
- Non-root user execution in containers  
- Network segmentation with dedicated Docker bridge network  
- Environment variables for all secrets (never hardcoded)  
- **`--forwarded-allow-ips`** restricted to internal network (not `*`)  
   
### Blockchain Security  
   
- EIP-712 typed data signing for payment authorizations (planned)  
- Nonce-based replay protection on all on-chain transactions (planned)  
- Payment verification via direct RPC node query (not event-only) — **stub documented, requires WEB3_RPC_URL**  
   
---  
   
## 🔴 GDPR / RGPD Compliance for Voice Data  
   
> **STATUS: IN PROGRESS — REQUIRED FOR EU MARKET ENTRY**  
   
### Why This Is Critical  
   
Processing voice data (biometric data under GDPR Article 9) is classified as **special category data**. Any business handling EU customers must comply with GDPR or face fines up to **4% of global annual turnover** or **€20 million**.  
   
### Implemented in v2.1  
   
| # | Requirement | Implementation | Status |  
|---|-------------|----------------|--------|  
| 1 | **Lawful Basis** | Explicit consent (Article 9) for voice recording & processing | 🟡 Stub |  
| 2 | **Data Processing Agreement (DPA)** | Signed DPA with Vapi, Twilio, OpenAI, and all sub-processors | ❌ Not Documented |  
| 3 | **Right to Erasure** | Automated deletion of call recordings & transcripts within 30 days of request | ✅ `erase_customer_data()` |  
| 4 | **Data Minimization** | Auto-delete recordings after configurable retention period (default: 90 days) | ✅ `purge_expired_voice_data()` |  
| 5 | **Privacy by Design** | Voice data encrypted at rest (AES-256) and in transit (TLS 1.3) | 🟡 TLS 1.3 via Nginx |  
| 6 | **Consent Logging** | Immutable audit trail of consent timestamps per caller | ✅ `ConsentRecord` SQLAlchemy model |  
| 7 | **Data Localization** | EU-based data residency option (Frankfurt / Dublin region) | ❌ Not Implemented |  
| 8 | **Breach Notification** | 72-hour notification workflow to supervisory authority & affected users | ✅ `BreachLog` SQLAlchemy model |  
| 9 | **Privacy Policy** | Dedicated voice data processing clause in legal terms | ❌ Not Documented |  
| 10 | **DPO Contact** | Published Data Protection Officer contact for EU clients | ❌ Not Documented |  
   
### GDPR Implementation  
   
```python  
# backend/app/core/gdpr.py  
# Voice data retention & deletion scheduler  
   
from app.models.consent_record import ConsentRecord, BreachLog  
   
async def purge_expired_voice_data(db: AsyncSession, retention_days: int = 90):  
    """Delete voice recordings older than retention policy."""  
    cutoff = datetime.utcnow() - timedelta(days=retention_days)  
    expired_calls = await db.execute(delete(Call).where(Call.created_at < cutoff))  
    expired_sms = await db.execute(delete(SMSMessage).where(SMSMessage.created_at < cutoff))  
    await db.commit()  
    return {"calls_deleted": expired_calls.rowcount, "sms_deleted": expired_sms.rowcount}  
   
async def erase_customer_data(db: AsyncSession, customer_id: str, business_id: str):  
    """Right to Erasure (GDPR Article 17)."""  
    await db.execute(delete(Call).where(Call.customer_id == customer_id))  
    await db.execute(delete(SMSMessage).where(SMSMessage.customer_id == customer_id))  
    await db.execute(update(Customer).where(Customer.id == customer_id).values(  
        phone=None, email=None, name="[DELETED]", is_deleted=True  
    ))  
    await db.commit()  
```  
   
---  
   
## 🔴 Load Testing & Performance Benchmarks  
   
> **STATUS: NOT IMPLEMENTED — REQUIRED BEFORE PRODUCTION LAUNCH**  
   
### Required Benchmarks  
   
| Metric | Target | Test Tool |  
|--------|--------|-----------|  
| **Concurrent Calls** | 500 simultaneous | Locust / k6 |  
| **API Response Time (p95)** | < 200ms | Artillery |  
| **Database Queries** | < 50ms average | pgBench |  
| **WebSocket Latency** | < 100ms | WebSocket-bench |  
| **End-to-End Call Flow** | < 3s setup time | Custom Vapi stress test |  
| **Memory Leak** | 0% growth over 24h | Valgrind / memory_profiler |  
| **Crash Recovery** | < 30s auto-restart | Chaos Monkey / Docker restart |  
   
### Infrastructure Sizing  
   
| Tier | Expected Load | Recommended Infrastructure |  
|------|---------------|---------------------------|  
| **Basic** | 500 calls/month | 1x API (2 vCPU, 4GB RAM), 1x DB (1 vCPU, 2GB RAM) |  
| **Professional** | 2,000 calls/month | 2x API (load balanced), 1x DB (2 vCPU, 4GB RAM), 1x Redis |  
| **Enterprise** | 10,000 calls/month | 3x API (auto-scaling), 1x DB (4 vCPU, 8GB RAM), 2x Redis (HA), CDN |  
   
---  
   
## 🔴 CI/CD Pipeline  
   
> **STATUS: PROVIDED — SEE `.github/workflows/ci-cd.yml`**  
   
### Required Pipeline Stages  
   
| Stage | Tool | Purpose |  
|-------|------|---------|  
| **Lint** | Ruff / Black / ESLint | Code style consistency |  
| **Unit Tests** | pytest / Jest | Logic correctness |  
| **Integration Tests** | pytest + Testcontainers | DB & external API interaction |  
| **SAST** | Bandit / Semgrep | Static security analysis |  
| **Dependency Scan** | Safety / Snyk | Known vulnerabilities in packages |  
| **Container Scan** | Trivy / Snyk | OS & image vulnerabilities |  
| **Coverage Gate** | Codecov | Minimum 80% coverage block |  
| **E2E Tests** | Playwright / Cypress | Full user journey validation |  
   
---  
   
## 🔴 Monitoring & Observability  
   
> **STATUS: IMPLEMENTED — SEE `backend/app/core/monitoring.py`**  
   
### Required Observability Stack  
   
| Layer | Tool | Purpose | Cost (approx) |  
|-------|------|---------|---------------|  
| **Metrics** | Prometheus + Grafana | CPU, memory, request rate, latency | Free (self-hosted) |  
| **Logs** | Loki + Grafana | Centralized log aggregation | Free (self-hosted) |  
| **Traces** | Jaeger / Tempo | Distributed request tracing | Free (self-hosted) |  
| **APM** | Datadog / New Relic | Application performance monitoring | $70-150/mo |  
| **Uptime** | UptimeRobot / Pingdom | External health checks | $15/mo |  
| **Error Tracking** | Sentry | Real-time exception alerting | $26/mo |  
| **Alerting** | PagerDuty / Opsgenie | On-call rotation & escalation | $29/user/mo |  
   
### Key Metrics to Track  
   
| Metric | Alert Threshold | Action |  
|--------|-----------------|--------|  
| API Error Rate | > 1% | Page on-call engineer |  
| API Latency (p99) | > 500ms | Scale API containers |  
| DB Connection Pool | > 80% usage | Increase pool size or shard |  
| Redis Memory | > 85% usage | Evict old cache or scale |  
| Failed Calls (Vapi) | > 5% in 5min | Check Vapi status page |  
| Webhook Queue Depth | > 1000 pending | Scale Celery workers |  
| Disk Usage | > 85% | Trigger backup cleanup |  
   
---  
   
## 🔴 Automated Database Backup & Disaster Recovery  
   
> **STATUS: PROVIDED — SEE `scripts/backup-database.sh`**  
   
### Required Backup Strategy  
   
| Layer | Frequency | Retention | Tool |  
|-------|-----------|-----------|------|  
| **PostgreSQL Full Backup** | Daily at 02:00 UTC | 30 days | pg_dump + S3 |  
| **PostgreSQL WAL Archive** | Continuous | 7 days | WAL-G / pgBackRest |  
| **Redis RDB Snapshot** | Every 6 hours | 7 days | Redis BGSAVE + S3 |  
| **S3 Object Backup** | Real-time replication | Cross-region | S3 Cross-Region Replication |  
| **Disaster Recovery** | Quarterly drill | N/A | Automated failover test |  
   
---  
   
## Changelog  
   
### v2.1 (2026-06-16) — Némésis Security Review  
   
- **Security**: Redis-backed token blacklist, brute force, rate limiting  
- **Auth**: Refresh token rotation, password reset via SendGrid, logout revocation  
- **Webhooks**: Correct algorithms per provider (Twilio SHA1, Vapi HMAC-SHA256)  
- **GDPR**: Persistent consent records and breach logs in PostgreSQL  
- **Appointments**: SELECT FOR UPDATE race condition fix  
- **Settings**: SSRF protection + httpx async  
- **Web3**: On-chain verification stub (documented, requires RPC node)  
- **Monitoring**: /metrics protected by API key  
   
### v2.0 (2026-06-16) — Initial Architecture  
   
- Complete API design with 55 endpoints  
- Docker multi-stage builds  
- CI/CD pipeline template  
- Prometheus metrics  
- Backup scripts  
   
---  
   
## Project Structure  
   
```  
ai-receptionist/  
├── backend/              # FastAPI application  
│   ├── app/  
│   │   ├── api/          # Route handlers (all endpoints defined, ~30 implemented)  
│   │   ├── core/         # Config, security, logging, gdpr, monitoring, token_store  
│   │   ├── db/           # Database engine, base, sessions  
│   │   ├── integrations/ # External service integrations (Vapi, Twilio, Web3 stubs)  
│   │   ├── models/       # SQLAlchemy models (incl. ConsentRecord, BreachLog)  
│   │   ├── schemas/      # Pydantic schemas (strict validation)  
│   │   ├── services/     # Business logic (tier management)  
│   │   └── main.py       # Application entry (middleware stack)  
│   ├── migrations/       # Alembic migrations (config ready)  
│   ├── tests/            # Test suite (structure ready)  
│   ├── Dockerfile        # Dev container  
│   ├── Dockerfile.prod   # Production container (multi-stage)  
│   ├── requirements.txt  
│   └── .env.example      # Environment template  
├── frontend/             # React 19 SPA  
│   ├── src/  
│   ├── public/  
│   ├── Dockerfile  
│   ├── Dockerfile.prod   # Production (Vite → Nginx)  
│   └── package.json  
├── infra/                # Infrastructure  
│   ├── docker-compose.yml      # Development stack  
│   ├── docker-compose.prod.yml # Production stack  
│   └── nginx.conf              # Nginx reverse proxy  
├── scripts/              # Operational scripts  
│   ├── backup-database.sh      # DB backup to S3  
│   └── init-letsencrypt.sh   # SSL certificate init  
├── docs/                 # Documentation  
│   ├── ARCHITECTURE.md   # System architecture  
│   ├── API.md            # Complete API reference  
│   └── PRICING.md        # Pricing & ROI guide  
├── .github/              # GitHub Actions  
│   └── workflows/  
│       └── ci-cd.yml     # Full CI/CD pipeline  
├── .gitignore  
├── CONTRIBUTING.md  
├── LICENSE  
└── README.md  
```  
   
---  
   
## 🚀 Just Starting Out?  
   
This Enterprise architecture is designed for **chains, agencies, and corporate clients** who need multi-tenant SaaS with subscription billing.  
   
If you're a **freelance developer** or a **solo clinic owner** looking for:  
- A simpler, faster deployment (no Docker, no Redis)  
- One-time $2,500 setup instead of monthly subscriptions  
- Direct ownership of your Vapi/Twilio accounts  
- A lightweight dashboard that just works  
- GDPR erase, quiet hours SMS, emergency transfer, and calendar conflict detection out of the box  
   
**→ Check out [AI Receptionist Pro](https://github.com/mailtkarim-bot/AI_Receptionist_Pro)**    
The same core technology, packaged for rapid freelance deployment.  
   
---  
   
## Contributing  
   
This is a **portfolio project** demonstrating full-stack SaaS architecture skills. While I welcome feedback and suggestions, please note that this is primarily a **learning and demonstration repository**.  
   
### Development Setup  
   
```  
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
   
This project is licensed under the **MIT License** — see LICENSE for details.  
   
---  
   
<div align="center">  
   
**Built with ❤️ in Dubai**    
*"Enterprise-grade AI voice architecture. Demonstrated. Documented. Ready for your review."*  
   
</div>  
