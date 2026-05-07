# 🛒 ProductIntel

> AI-powered e-commerce product research intelligence platform. Replace 5–10 hours of manual research with a single query.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![MiniMax](https://img.shields.io/badge/MiniMax%20M2.7-AI-orange)](https://www.minimaxi.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Coolify](https://img.shields.io/badge/Coolify-Ready-6366f1)](https://coolify.io)

---

## 🚀 What It Does

- **Facebook Ad Library** → Scans active ads, calculates ad duration momentum
- **Alibaba** → Extracts MOQ, pricing, supplier ratings
- **Amazon PA API 5.0** → Reviews, pricing, sentiment (with HTML fallback)
- **Google Trends** → Demand validation via pytrends-modern
- **MiniMax M2.7** → 3-pass AI analysis chain (normalize → compete → verdict)

### Verdict System
| Score | Verdict | Action |
|---|---|---|
| 70-100 | **PURSUE** | Strong signals, enter market |
| 45-69 | **RISKY** | Mixed signals, proceed with caution |
| 0-44 | **SKIP** | Weak demand or oversaturated |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  React 19 + Tailwind + Vite (Frontend)                     │
│  Dark neon UI · Glassmorphism · Real-time progress          │
└──────────────────────────────┬────────────────────────────────┘
                               │ HTTPS / API
┌──────────────────────────────▼────────────────────────────────┐
│  FastAPI + Python 3.12 (Backend)                             │
│  Auth · Rate Limiting · Circuit Breakers · Multi-tenancy      │
└──────────────────────────────┬────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌───────────────┐  ┌──────────────────┐  ┌─────────────────┐
│  PostgreSQL 16  │  │  Redis 7.2       │  │  Celery Workers │
│  (Primary DB)   │  │  Cache + Queue   │  │  Scrapers + AI  │
└─────────────────┘  └──────────────────┘  └─────────────────┘
```

---

## 📦 Open Source Scraper Integration Plan

### Facebook Ads → `minimaxir/facebook-ad-library-scraper` (forked + modernized)
- ✅ Original Graph API logic is sound
- 🔄 **Modernized**: async httpx, v19.0 API, `ad_type=ALL`
- 🔄 **Token pool**: automatic rotation + Playwright fallback
- ⏱️ Saves ~1 week of API pagination engineering

### Alibaba → `scraper-bank/Alibaba.com-Scrapers` (direct use)
- ✅ Production-ready Python + Node.js implementations
- ✅ Playwright + Puppeteer + ScrapeOps proxy support
- 🔄 Swapped ScrapeOps for Bright Data credentials
- ⏱️ Saves 2–3 weeks of proxy integration

### Amazon → `scrapfly/scrapfly-scrapers` (fallback)
- ✅ XPath/CSS selectors kept up-to-date
- ✅ Amazon PA API 5.0 as primary source (official, free)
- 🔄 Fallback to scrapfly-style HTML scraper on rate limits
- ⏱️ Saves selector maintenance overhead

### Google Trends → `pytrends-modern` (NOT pytrends)
- ⚠️ `pytrends` was **archived April 17, 2025** — no replacement
- ✅ `pytrends-modern` combines pytrends + trendspyg + new features
- ✅ RSS feed support (0.2s), async, active maintenance
- ⏱️ Critical swap — prevents silent breakage

---

## 🐳 Docker + Coolify Deployment

### Local Development
```bash
# Clone repo
cd productintel

# Copy env
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# API:      http://localhost:8000
# API Docs: http://localhost:8000/docs
# Flower:   http://localhost:5555
```

### Coolify Self-Hosted
1. Push repo to GitHub
2. In Coolify: **Create Resource** → **Docker Compose**
3. Point to your repo
4. Add environment variables from `.env.example`
5. Deploy

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| AI | MiniMax M2.7 (1M context) |
| Backend | FastAPI 0.115 + Python 3.12 |
| Frontend | React 19 + Vite + Tailwind CSS |
| UI | shadcn/ui + Custom glassmorphism |
| Queue | Celery 5.4 + Redis 7.2 |
| Database | PostgreSQL 16 + asyncpg |
| Scraping | Playwright + httpx + tenacity |
| Auth | JWT (RS256) + bcrypt |

---

## 🎯 Pricing Tiers

| Plan | Price | Analyses | Watchlist | Exports |
|---|---|---|---|---|
| Starter | $49/mo | 50/day | 10 | 5/mo |
| Pro | $149/mo | 500/day | 100 | 50/mo |
| Agency | $499/mo | 5000/day | 1000 | 500/mo |

---

## 📝 License

MIT — Built for dropshippers, Amazon sellers, and Shopify merchants.

---

*Powered by MiniMax M2.7 · Forked from minimaxir · Inspired by scraper-bank & scrapfly*