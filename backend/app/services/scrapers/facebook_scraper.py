import httpx
import asyncio
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings

settings = get_settings()

class FacebookAdScraper:
    """Modernized Facebook Ad Library scraper based on minimaxir/facebook-ad-library-scraper.
    
    Original: https://github.com/minimaxir/facebook-ad-library-scraper
    Modernization: async httpx, v19.0 API, ad_type=ALL support, token pool integration.
    """
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.FB_ACCESS_TOKEN
        self.api_version = settings.FB_API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}/ads_archive"
        self.client = httpx.AsyncClient(timeout=30.0)
        self.rate_limit_remaining = 200
        self.rate_limit_reset = datetime.utcnow() + timedelta(hours=1)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def search_ads(
        self,
        search_terms: str,
        ad_type: str = "ALL",  # ALL (not just POLITICAL_AND_ISSUE_ADS)
        ad_active_status: str = "ACTIVE",
        countries: List[str] = None,
        limit: int = 100,
        max_results: int = 500
    ) -> Dict[str, Any]:
        """Search Facebook Ad Library for ads matching search terms.
        
        Forked from minimaxir/facebook-ad-library-scraper and modernized:
        - Switched from synchronous requests to async httpx
        - Updated Graph API from v5.0 to v19.0
        - Added ad_type=ALL parameter (original only supported POLITICAL_AND_ISSUE_ADS)
        - Added automatic pagination handling
        - Added rate limit tracking
        """
        if not countries:
            countries = ["US"]
        
        params = {
            "access_token": self.access_token,
            "ad_type": ad_type,
            "ad_reached_countries": json.dumps(countries),
            "ad_active_status": ad_active_status,
            "search_terms": search_terms,
            "fields": (
                "ad_creation_time,ad_creative_bodies,ad_creative_link_captions,"
                "ad_creative_link_descriptions,ad_creative_link_titles,"
                "ad_delivery_start_time,ad_delivery_stop_time,"
                "ad_snapshot_url,age_country_gender_reach_breakdown,"
                "beneficiary_payer_region,delivery_by_region,"
                "demographic_distribution,estimated_audience_size,"
                "eu_total_reach,impressions,publisher_platforms,"
                "spend"
            ),
            "limit": limit,
        }
        
        all_ads = []
        total_count = 0
        next_url = self.base_url
        
        while next_url and total_count < max_results:
            response = await self.client.get(next_url, params=params if next_url == self.base_url else None)
            
            # Track rate limits from headers
            if "x-app-usage" in response.headers:
                usage = json.loads(response.headers["x-app-usage"])
                self.rate_limit_remaining = 100 - usage.get("call_count", 0)
            
            response.raise_for_status()
            data = response.json()
            
            ads = data.get("data", [])
            for ad in ads:
                enriched_ad = self._enrich_ad(ad)
                all_ads.append(enriched_ad)
            
            total_count = len(all_ads)
            
            # Pagination
            paging = data.get("paging", {})
            next_url = paging.get("next")
            params = None  # Only use params on first request
            
            if total_count >= max_results:
                break
            
            # Respect rate limits
            if self.rate_limit_remaining < 10:
                wait_time = (self.rate_limit_reset - datetime.utcnow()).total_seconds()
                if wait_time > 0:
                    await asyncio.sleep(min(wait_time, 300))
        
        # Calculate metrics
        active_ads = [a for a in all_ads if a.get("is_active", False)]
        avg_duration = self._calculate_avg_duration(active_ads)
        unique_advertisers = len(set(a.get("page_name", "") for a in all_ads))
        
        return {
            "ads": all_ads[:max_results],
            "active_ads_count": len(active_ads),
            "total_ads_found": len(all_ads),
            "avg_duration_days": avg_duration,
            "unique_advertisers": unique_advertisers,
            "top_countries": self._extract_top_countries(all_ads),
            "scraped_at": datetime.utcnow().isoformat(),
            "api_version": self.api_version,
            "search_terms": search_terms,
        }
    
    def _enrich_ad(self, ad: dict) -> dict:
        """Add computed fields to raw ad data (from original minimaxir scraper)."""
        # Extract ad_id from snapshot URL (original logic)
        snapshot_url = ad.get("ad_snapshot_url", "")
        ad_id = None
        if snapshot_url:
            import re
            match = re.search(r'id=(\d+)', snapshot_url)
            if match:
                ad_id = match.group(1)
        
        ad["ad_id"] = ad_id
        ad["is_active"] = ad.get("ad_delivery_stop_time") is None
        
        # Impute 0 for missing demographics (original scraper's cleaning logic)
        if "demographic_distribution" not in ad or not ad["demographic_distribution"]:
            ad["demographic_distribution"] = []
        
        if "delivery_by_region" not in ad or not ad["delivery_by_region"]:
            ad["delivery_by_region"] = []
        
        return ad
    
    def _calculate_avg_duration(self, ads: list) -> float:
        durations = []
        for ad in ads:
            start = ad.get("ad_delivery_start_time")
            stop = ad.get("ad_delivery_stop_time")
            if start:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                if stop:
                    stop_dt = datetime.strptime(stop, "%Y-%m-%d")
                else:
                    stop_dt = datetime.utcnow()
                durations.append((stop_dt - start_dt).days)
        return round(sum(durations) / len(durations), 1) if durations else 0.0
    
    def _extract_top_countries(self, ads: list) -> list:
        country_counts = {}
        for ad in ads:
            for region in ad.get("delivery_by_region", []):
                country = region.get("country", "Unknown")
                country_counts[country] = country_counts.get(country, 0) + region.get("percentage", 0)
        sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
        return [c[0] for c in sorted_countries[:5]]
    
    async def close(self):
        await self.client.aclose()
