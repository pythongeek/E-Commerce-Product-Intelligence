import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pytrends_modern import PyTrends
from app.core.config import get_settings

settings = get_settings()

class GoogleTrendsScraper:
    """Google Trends scraper using pytrends-modern (NOT pytrends - archived April 2025).
    
    pytrends was archived on April 17, 2025 with no replacement.
    pytrends-modern combines pytrends + trendspyg + google-trends features with:
    - RSS Feed support (0.2s vs 10s)
    - Enhanced error handling with auto retry
    - Async support
    - Active maintenance
    
    Critical swap: using pytrends-modern instead of dead pytrends.
    """
    
    def __init__(self):
        self.py_trends = None
        self.rss = None
    
    def _get_client(self):
        """Lazy initialization of PyTrends client."""
        if self.py_trends is None:
            self.py_trends = PyTrends(hl='en-US', tz=360, timeout=(10, 25), retries=2)
        return self.py_trends
    
    async def get_interest_over_time(
        self,
        keywords: list[str],
        timeframe: str = "today 3-m",
        geo: str = "US"
    ) -> Dict[str, Any]:
        """Get Google Trends interest over time data."""
        try:
            client = self._get_client()
            
            # Build payload
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, client.build_payload, keywords, cat=0, timeframe=timeframe, geo=geo)
            
            # Get interest over time
            df = await loop.run_in_executor(None, client.interest_over_time)
            
            if df is None or df.empty:
                return {"trend_data": [], "is_rising": False, "peak_interest": 0}
            
            # Calculate trend metrics
            trend_data = []
            for col in keywords:
                if col in df.columns:
                    values = df[col].tolist()
                    trend_data.append({
                        "keyword": col,
                        "avg_interest": round(sum(values) / len(values), 1),
                        "peak_interest": max(values),
                        "current_interest": values[-1] if values else 0,
                        "data_points": len(values),
                    })
            
            # Determine if trend is rising
            is_rising = False
            if trend_data:
                latest = [t["current_interest"] for t in trend_data]
                avg = [t["avg_interest"] for t in trend_data]
                is_rising = sum(latest) / len(latest) > sum(avg) / len(avg) if avg else False
            
            return {
                "trend_data": trend_data,
                "is_rising": is_rising,
                "peak_interest": max(t["peak_interest"] for t in trend_data) if trend_data else 0,
                "timeframe": timeframe,
                "geo": geo,
                "scraped_at": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            return {"error": str(e), "trend_data": [], "is_rising": False}
    
    async def get_related_queries(
        self,
        keywords: list[str],
        geo: str = "US"
    ) -> Dict[str, Any]:
        """Get related queries for trend keywords."""
        try:
            client = self._get_client()
            loop = asyncio.get_event_loop()
            
            await loop.run_in_executor(None, client.build_payload, keywords, cat=0, timeframe="today 3-m", geo=geo)
            
            related = await loop.run_in_executor(None, client.related_queries)
            
            results = {}
            if related:
                for keyword in keywords:
                    if keyword in related and related[keyword]:
                        top = related[keyword].get("top", [])
                        rising = related[keyword].get("rising", [])
                        results[keyword] = {
                            "top_queries": top[:10] if isinstance(top, list) else [],
                            "rising_queries": rising[:10] if isinstance(rising, list) else [],
                        }
            
            return {
                "related_queries": results,
                "scraped_at": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def get_trending_searches(self, geo: str = "US") -> Dict[str, Any]:
        """Get real-time trending searches using RSS feed (0.2s, from trendspyg)."""
        try:
            from pytrends_modern import TrendsRSS
            
            rss = TrendsRSS()
            trends = rss.get_trends(geo=geo)
            
            return {
                "trending_searches": trends,
                "count": len(trends),
                "geo": geo,
                "scraped_at": datetime.utcnow().isoformat(),
                "source": "rss_feed",
            }
            
        except Exception as e:
            return {"error": str(e)}
