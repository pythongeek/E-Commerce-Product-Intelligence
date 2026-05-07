import asyncio
import json
import hashlib
import hmac
import datetime
from typing import Optional, Dict, Any, List
import httpx
from app.core.config import get_settings

settings = get_settings()

class AmazonPAAPI:
    """Amazon Product Advertising API 5.0 client.
    
    Primary data source for Amazon reviews and pricing.
    Falls back to scrapfly/scrapfly-scrapers HTML scraper when rate limited.
    """
    
    def __init__(self):
        self.access_key = settings.AMAZON_PA_API_KEY
        self.secret_key = settings.AMAZON_PA_API_SECRET
        self.partner_tag = settings.AMAZON_ASSOCIATE_TAG
        self.region = settings.AMAZON_REGION
        self.host = f"webservices.amazon.{self._get_domain()}"
        self.uri = "/paapi5/searchitems"
        self.service = "ProductAdvertisingAPI"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _get_domain(self) -> str:
        domain_map = {
            "us-east-1": "com",
            "eu-west-1": "co.uk",
            "ap-northeast-1": "co.jp",
        }
        return domain_map.get(self.region, "com")
    
    def _sign(self, key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
    
    def _get_signature_key(self, secret: str, date_stamp: str) -> bytes:
        k_date = self._sign(("AWS4" + secret).encode("utf-8"), date_stamp)
        return k_date
    
    def _build_headers(self, payload: dict) -> dict:
        t = datetime.datetime.utcnow()
        amz_date = t.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = t.strftime("%Y%m%d")
        
        payload_bytes = json.dumps(payload).encode("utf-8")
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()
        
        headers = {
            "host": self.host,
            "x-amz-date": amz_date,
            "x-amz-target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems",
            "content-type": "application/json",
            "content-encoding": "amz-1.0",
        }
        
        # For simplicity in MVP, using a simplified signing approach
        # Full AWS SigV4 implementation would go here
        return headers
    
    async def search_items(
        self,
        keywords: str,
        search_index: str = "All",
        item_count: int = 10
    ) -> Dict[str, Any]:
        """Search Amazon products using PA API 5.0."""
        payload = {
            "Keywords": keywords,
            "SearchIndex": search_index,
            "ItemCount": item_count,
            "Resources": [
                "Images.Primary.Medium",
                "ItemInfo.Title",
                "Offers.Listings.Price",
                "CustomerReviews.StarRating",
                "BrowseNodeInfo.BrowseNodes",
            ],
            "PartnerTag": self.partner_tag,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com",
        }
        
        try:
            headers = self._build_headers(payload)
            response = await self.client.post(
                f"https://{self.host}{self.uri}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            items = data.get("SearchResult", {}).get("Items", [])
            return self._normalize_items(items)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return {"error": "Amazon PA API rate limited", "fallback_needed": True}
            return {"error": f"Amazon API error: {e.response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _normalize_items(self, items: list) -> dict:
        products = []
        for item in items:
            info = item.get("ItemInfo", {})
            offers = item.get("Offers", {})
            reviews = item.get("CustomerReviews", {})
            images = item.get("Images", {})
            
            product = {
                "asin": item.get("ASIN"),
                "title": info.get("Title", {}).get("DisplayValue"),
                "price_usd": offers.get("Listings", [{}])[0].get("Price", {}).get("Amount") if offers.get("Listings") else None,
                "rating": reviews.get("StarRating", {}).get("Value"),
                "image_url": images.get("Primary", {}).get("Medium", {}).get("URL"),
                "detail_url": item.get("DetailPageURL"),
            }
            products.append(product)
        
        # Aggregate stats
        prices = [p["price_usd"] for p in products if p.get("price_usd")]
        ratings = [p["rating"] for p in products if p.get("rating")]
        
        return {
            "products": products,
            "avg_selling_price_usd": round(sum(prices) / len(prices), 2) if prices else None,
            "avg_rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
            "total_reviews": sum(1 for p in products if p.get("rating")),
            "scraped_at": datetime.datetime.utcnow().isoformat(),
        }
    
    async def close(self):
        await self.client.aclose()


class AmazonFallbackScraper:
    """Fallback HTML scraper using scrapfly-style XPath/CSS selectors.
    
    Based on scrapfly/scrapfly-scrapers amazon-scraper selectors.
    Used when PA API hits rate limits.
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )
    
    async def search_items(self, keywords: str) -> dict:
        """Scrape Amazon search results using CSS selectors (scrapfly-style)."""
        from bs4 import BeautifulSoup
        import urllib.parse
        
        url = f"https://www.amazon.com/s?k={urllib.parse.quote(keywords)}"
        
        try:
            response = await self.client.get(url)
            if response.status_code == 503:
                return {"error": "Amazon blocked (503)", "fallback_needed": False}
            
            soup = BeautifulSoup(response.text, "lxml")
            
            # scrapfly-style selectors
            items = soup.select("[data-component-type='s-search-result']")
            
            products = []
            for item in items[:10]:
                title_el = item.select_one("h2 a span") or item.select_one(".s-size-mini span")
                price_el = item.select_one(".a-price .a-offscreen")
                rating_el = item.select_one(".a-icon-alt")
                img_el = item.select_one(".s-image")
                
                title = title_el.get_text(strip=True) if title_el else ""
                price_text = price_el.get_text(strip=True) if price_el else ""
                rating_text = rating_el.get_text(strip=True) if rating_el else ""
                img_url = img_el.get("src") if img_el else ""
                
                price = self._parse_price(price_text)
                rating = self._parse_rating(rating_text)
                
                products.append({
                    "title": title,
                    "price_usd": price,
                    "rating": rating,
                    "image_url": img_url,
                })
            
            prices = [p["price_usd"] for p in products if p.get("price_usd")]
            ratings = [p["rating"] for p in products if p.get("rating")]
            
            return {
                "products": products,
                "avg_selling_price_usd": round(sum(prices) / len(prices), 2) if prices else None,
                "avg_rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
                "total_reviews": len(products),
                "source": "fallback_html_scraper",
                "scraped_at": datetime.datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_price(self, text: str) -> Optional[float]:
        import re
        numbers = re.findall(r'[\d,]+\.\d+', text.replace(",", ""))
        return float(numbers[0]) if numbers else None
    
    def _parse_rating(self, text: str) -> Optional[float]:
        import re
        match = re.search(r'(\d+\.?\d*)\s*out of\s*5', text)
        return float(match.group(1)) if match else None
    
    async def close(self):
        await self.client.aclose()
