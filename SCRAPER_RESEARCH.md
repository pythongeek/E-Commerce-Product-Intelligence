# Open-Source Scraper Research & Ratings
## ProductIntel Use Case — E-Commerce Product Intelligence

---

## Executive Summary

| Source | Recommended Scraper | Rating | Integration Effort | Maintenance Risk |
|---|---|---|---|---|
| **Facebook Ad Library** | `minimaxir/facebook-ad-library-scraper` (forked) | ⭐⭐⭐⭐ | 1 week | Medium |
| **Alibaba.com** | `scraper-bank/Alibaba.com-Scrapers` | ⭐⭐⭐⭐⭐ | 2-3 days | Low |
| **Amazon** | `scrapfly/scrapfly-scrapers` (fallback) | ⭐⭐⭐⭐ | 3 days | Low |
| **Google Trends** | `pytrends-modern` (NOT pytrends) | ⭐⭐⭐⭐⭐ | 1 day | Low |

---

## 1. Facebook Ad Library

### Option A: `minimaxir/facebook-ad-library-scraper` ⭐⭐⭐⭐ RECOMMENDED
- **GitHub**: https://github.com/minimaxir/facebook-ad-library-scraper
- **Stars**: 133 | **Last Update**: 2019 (archived logic)
- **License**: MIT

**Why it was chosen:**
- The original Graph API pagination logic is sound and battle-tested
- Uses official Facebook Ad Library API (not scraping — legal)
- Already handles weird FB data encoding decisions (demographic imputation)

**Modernization required:**
- ✅ Switched from `requests` → `async httpx`
- ✅ Updated Graph API from `v5.0` → `v19.0`
- ✅ Added `ad_type=ALL` parameter (original only supported `POLITICAL_AND_ISSUE_ADS`)
- ✅ Added automatic pagination handling
- ✅ Added rate limit tracking per token
- ✅ Wrapped in token pool + Playwright fallback architecture

**Production concerns:**
- FB tokens expire every 60-90 days → token pool manager required
- Rate limit: 200 calls/hour/token → need multiple tokens for scale
- API version deprecates annually → version bump needed yearly

**Rating: 8/10** — Best starting point, requires active token management.

---

### Option B: `apify/facebook-ads-library-scraper` ⭐⭐⭐
- **Platform**: Apify actor (not pure open-source)
- **Pricing**: Free tier limited, then paid
- **Verdict**: Good for no-code users, but Apify lock-in is a concern for a SaaS product.

---

### Option C: `abdulmanan45/facebook-ads-scraper` ⭐⭐
- **Approach**: Selenium browser automation
- **Risk**: Higher detection/blocking, DOM breaks when Meta updates
- **Verdict**: Not recommended for production — too brittle.

---

## 2. Alibaba.com

### Option A: `scraper-bank/Alibaba.com-Scrapers` ⭐⭐⭐⭐⭐ RECOMMENDED
- **GitHub**: https://github.com/scraper-bank/Alibaba.com-Scrapers
- **Stars**: N/A (newer org)
- **License**: MIT

**Why it was chosen:**
- Production-ready with both Python and Node.js implementations
- Uses Playwright, Puppeteer, BeautifulSoup, Cheerio, Selenium
- ScrapeOps proxy support baked in (easy to swap for Bright Data)
- JSONL output format (streamable, database-friendly)
- Handles Alibaba's dynamic JavaScript rendering properly

**Integration approach:**
- Swapped ScrapeOps proxy for Bright Data residential credentials
- Wrapped in Celery task with circuit breaker
- Added human-like delays (1.5-4s random)
- Added CAPTCHA detection and graceful failure

**Rating: 9/10** — Most complete Alibaba scraper collection available. Swap proxy provider and it's production-ready.

---

### Option B: `scrapehero/alibaba-scraper` ⭐⭐⭐
- **Approach**: Scrapy + Selectorlib
- **Age**: 2018, limited maintenance
- **Verdict**: Simpler but less robust than scraper-bank. Good for learning.

---

## 3. Amazon

### Option A: Amazon PA API 5.0 (Official) ⭐⭐⭐⭐⭐ PRIMARY
- **Method**: Official API
- **Cost**: Free (up to limits)
- **Legal**: ✅ Fully compliant

**Why it's primary:**
- Official, legal, no ToS risk
- Structured JSON data for reviews, pricing, ratings
- No HTML parsing brittleness

**Fallback needed because:**
- Rate limits can be hit during bulk analysis
- Requires Associate account approval
- Some product categories have limited data

---

### Option B: `scrapfly/scrapfly-scrapers` ⭐⭐⭐⭐ FALLBACK RECOMMENDED
- **GitHub**: https://github.com/scrapfly/scrapfly-scrapers
- **Contains**: `amazon-scraper/` directory with maintained selectors
- **Approach**: XPath/CSS selector-based HTML scraping

**Why it was chosen as fallback:**
- The XPath/CSS selectors for Amazon's HTML are the most brittle part of any scraper
- This repo keeps selectors up-to-date across 40+ sites
- Fully async httpx (matches our stack)
- Easy to integrate as fallback when PA API rate limits

**Integration:**
- Use PA API 5.0 as primary source
- When `429` or missing data → fall back to scrapfly-style HTML scraper
- Wrapped in circuit breaker to prevent cascade failures

**Rating: 8/10** — Essential fallback, selector maintenance handled by community.

---

### Option C: `rainforest-api` / `DataForSEO` ⭐⭐⭐
- **Approach**: Paid middleware APIs
- **Cost**: $22.50 per 10,000 terms (DataForSEO)
- **Verdict**: Good for legal compliance but adds cost. Use if Amazon PA API is insufficient.

---

## 4. Google Trends

### Option A: `pytrends-modern` ⭐⭐⭐⭐⭐ CRITICAL SWAP
- **PyPI**: `pytrends-modern`
- **GitHub**: https://github.com/yiromo/pytrends-modern
- **Combines**: pytrends + trendspyg + google-trends features

**CRITICAL: `pytrends` was archived on April 17, 2025.**
- No replacement from original maintainers
- Any breaking changes from Google go unpatched
- Production pipelines using pytrends will silently break

**Why pytrends-modern was chosen:**
- ✅ All classic pytrends features (interest over time, by region, related queries)
- ✅ RSS Feed support: 0.2s vs 10s for trending data
- ✅ Enhanced error handling with exponential backoff
- ✅ Async support for concurrent requests
- ✅ Active maintenance (modern codebase)
- ✅ Full type hints

**Feature comparison:**

| Feature | pytrends | trendspyg | pytrends-modern |
|---|---|---|---|
| Interest Over Time | ✅ | ❌ | ✅ |
| Interest by Region | ✅ | ❌ | ✅ |
| Related Topics | ✅ | ❌ | ✅ |
| RSS Feed | ❌ | ✅ | ✅ |
| Async Support | ❌ | ❌ | ✅ |
| Active Maintenance | ❌ (archived) | ✅ | ✅ |
| Auto Retry | Partial | ✅ | ✅ |

**Rating: 9/10** — Critical swap that prevents production breakage.

---

## 5. Trustpilot

### Recommendation: Official Business API
- **Legal**: ✅ Official API
- **Cost**: Paid tier
- **Alternative**: Skip if unavailable (not core to scoring algorithm)
- **Note**: Never scrape Trustpilot without authorization — high legal risk.

---

## Integration Plan Summary

```
Facebook Ads    → fork minimaxir/facebook-ad-library-scraper
                  modernize to async, update to v19.0, add ad_type=ALL
                  wrap in token-pool + Playwright fallback
                  
Alibaba         → use scraper-bank/Alibaba.com-Scrapers directly
                  swap ScrapeOps for Bright Data
                  wrap in Celery + circuit breaker
                  
Amazon          → PA API 5.0 as PRIMARY (official, free)
                  scrapfly/scrapfly-scrapers as FALLBACK
                  selector maintenance handled by community
                  
Google Trends   → pytrends-modern (NOT pytrends)
                  pytrends was archived April 2025
                  this is a critical swap for production stability
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| FB API version deprecation | High | Medium | Annual version bump + token pool |
| Alibaba bot detection | Medium | Medium | Bright Data residential + stealth Playwright |
| Amazon PA API rate limit | High | Low | Fallback to HTML scraper |
| Google Trends API change | Medium | High | pytrends-modern active maintenance |
| Scraper selector breakage | Medium | Medium | Circuit breaker + graceful degradation |

---

*Research Date: 2026-05-08*
*Document Version: 1.0*
